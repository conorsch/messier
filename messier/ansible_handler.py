# -*- coding: utf-8 -*-
import yaml


class AnsibleHandler(object):

    def __init__(self):
        pass
        self.config = self.parse_messier_config()


    def parse_playbook(self):
        playbook = open(self.args['--playbook'], 'r')
        y = yaml.load(playbook)
        return [play['name'] for play in y]


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

