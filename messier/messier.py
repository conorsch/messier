# -*- coding: utf-8 -*-
import subprocess
import yaml

from .ansible_handler import AnsibleHandler
from .vagrant_handler import VagrantHandler
from .serverspec_handler import ServerspecHandler


class Messier(AnsibleHandler, VagrantHandler, ServerspecHandler):


    def __init__(self, args): 
        self.args = args
        AnsibleHandler.__init__(self)
        VagrantHandler.__init__(self)
        ServerspecHandler.__init__(self)
   


