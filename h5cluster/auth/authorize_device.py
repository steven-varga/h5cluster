# _____________________________________________________________________________
# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca
# _____________________________________________________________________________

import json
from logging import info, warning, critical
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
from auth0.v3.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier
from auth0.v3.authentication import Social
from auth0.v3.authentication.authorize_client import AuthorizeClient
from auth0.v3.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier, JwksFetcher
from auth0.v3.authentication import Passwordless
from auth0.v3.authentication.base import AuthenticationBase, Auth0Error
from auth0.v3.exceptions import TokenValidationError

from time import sleep
from ..utils.view import dict_view
from ..utils.progress import print_progress_bar
import webbrowser
from pathlib import Path
import jwt, sys

class AuthorizeDevice(AuthenticationBase):
    client_id = 'U8UA4KwGmgAYuXv1iww4C4uOuPH9UCH2'
    audience = 'https://h5cluster/'
    scope = 'email openid name email profile offline_access'
    domain = 'h5cluster.us.auth0.com'
    auth_token_file = Path(Path.home(), '.h5cluster.auth')
    algorithm="RS256"

    DISABLE_JWT_CHECKS = {
        "verify_signature": True,
        "verify_exp": False,
        "verify_nbf": False,
        "verify_iat": False,
        "verify_aud": False,
        "verify_iss": False,
        "require_exp": False,
        "require_iat": False,
        "require_nbf": False,
    } 

    def __init__(self): 
        super(AuthorizeDevice, self).__init__(self.domain)
        self.signature_verifier = AsymmetricSignatureVerifier('https://{}/.well-known/jwks.json'.format(self.domain))
        self.id_token_verifier = TokenVerifier(self.signature_verifier,
           'https://{}/'.format(self.domain), self.client_id)

    def poll_token(self, device_code):
        return self.post('https://{}/oauth/oauth/token'.format(self.domain), data = {
                'client_id': self.client_id, 'grant_type': 'urn:ietf:params:oauth:grant-type:device_code', 'device_code': device_code})

    def authorize(self):
        """Authorization code grant

        This is the OAuth 2.0 grant that regular web apps utilize in order to access an API.
        """
        reply = dict_view(
            self.post('https://{}/oauth/device/code'.format(self.domain), data = {
                'client_id': self.client_id, 'audience': self.audience, 'scope': self.scope}))
        webbrowser.open_new(reply.verification_uri_complete)
        info('authorization request: %s' % reply.verification_uri_complete)
        i, j = 0, 180

        print_progress_bar(0, j)
        while (j > i):
            i += 1
            sleep(1)
            print_progress_bar(i, j)
            if i % reply.interval: continue
            try:
                access_token = self.poll_token(reply.device_code)
                with open(self.auth_token_file, 'w') as fd_token:
                    json.dump(access_token, fd_token)
                print()
                return access_token
            except Auth0Error as err:
                if err.error_code != 'authorization_pending':
                    print()
                    critical(err) 
                    return None
        print()
        info('login expired, please try again...')
        return None
        
    def _fetch_key(self, key_id=None):
        return self.signature_verifier._fetcher.get_key(key_id)

    def decode_token(self, token):
        try:
            header = jwt.get_unverified_header(token)
        except jwt.exceptions.DecodeError:
            raise TokenValidationError("ID token could not be decoded.")

        alg = header.get('alg', None)

        kid = header.get('kid', None)
        secret_or_certificate = self._fetch_key(key_id=kid)

        try:
            decoded = jwt.decode(jwt=token, key=secret_or_certificate,
                                algorithms=[self.algorithm], options=self.DISABLE_JWT_CHECKS)
        except jwt.exceptions.InvalidSignatureError:
            raise TokenValidationError("Invalid token signature.")
        return decoded    


    def login(self):
        jwt_token = None
        try:
            with open(self.auth_token_file, 'r') as fd_token:
                jwt_token = json.load(fd_token)
            self.signature_verifier.verify_signature(jwt_token['access_token'])
        except Exception as err:
            jwt_token = self.authorize()
        finally:
            if jwt_token:
                at = dict_view(self.decode_token(jwt_token['access_token']))

                ut = dict_view(self.get(
                    url='https://{}/userinfo'.format(self.domain),
                    headers={'Authorization': 'Bearer {}'.format(jwt_token['access_token'])}))
                user = {
                    'permissions': at.permissions,
                    'name': ut.name,
                    'email': ut.email 
                }
                return dict_view(user)
            return dict_view({'permissions': [], 'name': '', 'email': ''})




    
