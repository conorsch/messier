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

