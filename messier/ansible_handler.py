# -*- coding: utf-8 -*-
import yaml


class AnsibleHandler(object):
    """
    Messier utility class for managing Ansible information.
    All methods are accessible via the Messier object. Call them from Messier.
    """

    def __init__(self):
        pass


    def parse_playbook(self):
        """
        Read testing playbook and return a list of `name` attributes for each task.
        This mirrors how `ansible_spec` determines Serverspec test runs.
        """
        playbook = open(self.args['--playbook'], 'r')
        y = yaml.load(playbook)
        return [play['name'] for play in y]

