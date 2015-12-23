# -*- coding: utf-8 -*-
import subprocess
import yaml
import os

from .ansible_handler import AnsibleHandler
from .vagrant_handler import VagrantHandler
from .serverspec_handler import ServerspecHandler

from contextlib import contextmanager



class Messier(AnsibleHandler, VagrantHandler, ServerspecHandler):


    def __init__(self, args): 
        self.args = args
        AnsibleHandler.__init__(self)
        VagrantHandler.__init__(self)
        ServerspecHandler.__init__(self)
        self.config = self.parse_messier_config()
   

    def parse_messier_config(self):
        try:
            config_file = open(self.args['--config'], 'r')
        except IOError:
            config = {}
        else:
            config = yaml.load(config_file)
            if not config:
                config = {}
        return config

    # Elegant solution from https://gist.github.com/LeoHuckvale/8f50f8f2a6235512827b
    # Stuffing this method into class because it's harder to reference otherwise
    @contextmanager
    def env_var(self, key, value):
        """
        Set environment variable for the context
        Example:
        --------
            with env_var('GIT_SSL_NO_VERIFY', '1'):
                # Environment variable is set here
                git.Repo.clone_from('https://giturl/user/project.git', 'some/dir')
            # Environment variable is reset here
        :param key: name of environment variable in dict :var:``os.environ``
        :param value: value to set for the context
        """
        old_value = os.environ.get(key, None)

        os.environ[key] = value

        yield

        if old_value is None:
            del os.environ[key]
        else:
            os.environ[key] = old_value

