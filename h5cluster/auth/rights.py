# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca

from .authorize_device import AuthorizeDevice

__user__ = None

    
def __has_flag(flag):
    global __user__
    if not __user__:
        __user__ = AuthorizeDevice().login()
    return  flag in __user__.permissions

def protect(arg):
    def my_protect(func):
        def inner(*args, **kwargs):
            if __has_flag(arg): func(*args, **kwargs)
        return inner
    return my_protect 

def access_token():
    return __user__.access_token

def login():
   return AuthorizeDevice().login() 