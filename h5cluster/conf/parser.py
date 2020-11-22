# -*- coding: utf-8 -*-
# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca

from logging import error, debug, exception, info
from configparser import SafeConfigParser, Error, NoSectionError, NoOptionError, DuplicateSectionError
import re
from inflection import camelize, underscore
import importlib

class ClusterConfigParser(SafeConfigParser):
    # list all default arguments in this dictionary, as it serves as fallback mechanism from
    # configuration file and arguments
    # all '-' is converted to '_' so vlaues can be used for function call dispatch
    # also used as a map for type conversion 
    __default_configuration__ = { 'size': 1, 'duration': 0, 'ami':'', 'ipv4':'', 'instance_type': 'm5d.large',
        'availability_zone': 'us-east-1a', 'udp_ports': '', 'tcp_ports': '22',
        'bid_price': '0.10', 'spot_request_size': 20, 'behavior': 'stop',
        'hostname_pattern': 'node%02i', 'hostname':'master', 'region': 'us-east-1',
        'volumes':[], 'services':[], 'nodes':[], 'dry_run': False}

    def __init__(self, path):
        '''initilizes parser object from ec2 configuration files

        Args:
            path (list): list to aws configuration files 
        '''
        # passing default configuration augments augments local configuration
        # with possibly missing values        
        super().__init__(strict=False, interpolation=None)
        # let's reduce clutter
        get = lambda name: self.get('completion', name).replace(' ','').split()
        try:
            self.read(path)
            # load in general completion from configuration files
            self.instances, self.regions = get('instances'), get('regions')
            # subtle!!! the dictinary names below must match with the `lambda` filter, as well as
            # the first component of the section names.
            self.volume, self.cluster, self.node, self.service = {}, {}, {}, {}
            for section in filter(lambda x: re.match('volume|service|cluster|node',x), self.sections()):
                k,v = section.split(' ')
                # 
                getattr(self,k)[v] = {k.replace('-','_'):v  for k,v  in dict(self[section]).items()}
            # now you can look up sections in relevant dictionaries to get values :) 
            # example to get volumes:
            # my_var = self.volume['ebs://xvy']
        except (Error, NoOptionError, DuplicateSectionError) as err:
            exception(err)
        except IOError as err:
            error('io error' + str(err))
        default_section = dict(self['default'])
        self.cluster['default'] = {**self.__default_configuration__, **default_section, **self.cluster['default']}

    def sget(self, section, name, field):
        '''retrieves the value of a field within a section of a configuration file, or
        __default_confiuration__ dictionary  

        Args:
            section (str): cluster | nodes | service | volume
            name (str): the component from url://name
            field (str): fields within a section

        Returns:
            str: the value of the referenced field
        '''
        name = name.strip() 
        try:
            return getattr(self, section)[name][field]
        except:
            return self.cluster['default'][field]

    def nodes(self, node_names):
        '''creates list of computer nodes from passed names, and relevant
        configuration settings/fields found in files used for initilizing.
        This method recursively parses `nodes`, `volumes`, `services` 

        Args:
            node_names (list): references node sections

        Returns:
            class `Node`: an instance on remote side
        '''
        nodes_ = []
        for name in node_names.split(','):
            name = name.strip()
            # using lambda function to ease on boiler plate
            get = lambda field: self.sget('node', name, field)
            args = {key:get(key) for key in ['ami', 'bid_price', 'instance_type', 'volumes', 'services', 'behavior', 'size']}
            v = dictionary_view(args)
            # `group` is same as `group_name in section `[node group_name] 
            v.group, v.size = name, int(v.size)
            # convert comma separated strings to list of objects:
            v.volumes, v.services = self.volumes(v.volumes), self.services(v.services)
            nodes_.append(Node(**args))
        return nodes_

    def dispatch(self, dict_name, uri):
        ''' delegates calls to `cluster.aws.[volume | service]` modules 
            and classes with camel case. 

        Args:
            dict_name (str): `service | volume` matching the classes in configuration files
            uri ([type]): [description]

        Returns:
            [class]: Ebs, Pvfs, ..., PvfsData, ... objects
        '''        
        split = lambda x: x.replace('-','_').split('://')
        # FIXME: add this feature
        if re.fullmatch(r'vol-[0-9a-z]{17}', uri):
            # used only with volumes, otherwise dispatched to  a stub
            return Ebs(**{'uri': uri, 'name': gen_token(4), 'type': 'ebs'})
        else:
            type_, name_ = split(uri)
            try: # actual dispatch to implementations
                args = getattr(self, dict_name)[uri] # look up arguments in
                # remove all white spaces from configuration values
                for k, v in args.items():
                    args[k] = ' '.join(v.split()) 
                # configuration file (stored as dictionary)
                args['type'], args['name'] = type_, name_ # augment the arguments with `name_` prop
                #delegate to `module.class` objects
                module = importlib.import_module('cluster.aws.' + dict_name)
                return getattr(module, camelize(type_))(**args)
            except KeyError as err:
                error('syntax error in configuration file: `' +  str(err)
                         +'` not specified in section `' + uri + '`')

    def volumes(self, volume_names):
        volumes_ = []
        for item in volume_names.split(','):
            if item: volumes_.append(self.dispatch('volume', item.strip()))
        # converted references to a list of volume objects
        return volumes_

    def services(self, service_names):
        services_ = []
        for item in service_names.split(','):
            if item: services_.append(self.dispatch('service', item.strip()))
        # converted references to a list of service objects
        return services_

    def update_with_arguments(self, args):
        '''`args` missing values are completed from the `[cluster current_name]` section
        of the configuration file, `[cluster default]` section or the internal 
        `__default_configuration__` dictionary

        Args:
            args (argparse): argparse values 

        Returns:
            object: the updated/completed arguments, where volumes, nodes, services
            are converted to parameterized objects, arguments are properties
        '''
        args_ = vars(args)
        # some arguments can only be set through configuration file, fetch them here
        if args_['cmd'] in ['start', 'add', 'configure']:
            args_['hostname_pattern'] = None
            for key, value in args_.items():
                # complete missing arguments from config file, relevant 
                # cluster section or default cluster
                if not value:
                    value = args_[key] = self.sget('cluster', args.cluster, key)
                if key in ['volumes', 'services', 'nodes']:
                    # dispatch to self.[volumes | services | nodes]
                    args_[key] = getattr(self, key)(args_[key])
                # convert to types as of default configuration
                if key in self.__default_configuration__.keys():
                    type_ = type(self.__default_configuration__[key])
                    args_[key] = type_(args_[key])
            # this is for `master` node only, rest of the nodes are handled in `def nodes(): ...`
            args_['group'], args_['size'] = 'master', 1
        # file system handlers
        if args_['cmd'] in ['mount', 'umount', 'mkfs']:
            for key, value in args_.items():
                try:
                    if not value: args_[key] = getattr(self, 'volume')[ args_['sub_cmd'] + '://' + args_['name']][key]
                except KeyError as err:
                    if key in self.cluster['default'].keys():
                        args_[key] = self.cluster['default'][key]
        # convert dictionary back to object.[properties]
        return args.cmd, args_