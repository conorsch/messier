# -*- coding: utf-8 -*-
import subprocess
import yaml

from .ansible_handler import AnsibleHandler
from .vagrant_handler import VagrantHandler


class Messier(AnsibleHandler, VagrantHandler):


    def __init__(self): 
        AnsibleHandler.__init__(self)
        VagrantHandler.__init__(self)
   


