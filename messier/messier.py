# -*- coding: utf-8 -*-
import subprocess
import yaml
import os

from .ansible_handler import AnsibleHandler
from .vagrant_handler import VagrantHandler
from .serverspec_handler import ServerspecHandler

from contextlib import contextmanager



class Messier(AnsibleHandler, VagrantHandler, ServerspecHandler):
    """
    Messier object for running multi-VM test suites. Interfaces with Vagrant
    for VM management, assumes Ansible as provisioner, and uses `ansible_spec`
    to run Serverspec tests.
    """

    def __init__(self, config_file=".messier", vms=None, provider="virtualbox", playbook=None):
        #self.args = args
        AnsibleHandler.__init__(self)
        VagrantHandler.__init__(self)
        ServerspecHandler.__init__(self)
        self.config = self.parse_messier_config(config_filepath=config_file)
        self.target_vms = vms
        self.provider = provider
        self.playbook = playbook
        # Inspect available VMs so exceptions are thrown early.
        self.vms


    @property
    def vms(self):
        """
        Return a list of Vagrant VM objects.
        """
        return self.available_vms(vms=self.target_vms)


    def parse_messier_config(self, config_filepath=".messier"):
        """
        Read YAML config file for Messier. Defaults to .messier.
        Supported options include:

          `serverspec_commands`: list of shell commands to run for Serverspec
          `serverspec_base_directory`: directory to cd into prior to running Serverspec
        """
        try:
            config_file = open(config_filepath,'r')
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

