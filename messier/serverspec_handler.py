# -*- coding: utf-8 -*-
import subprocess
from contextlib import contextmanager
import os


# Magnificent StackOverflow answer: http://stackoverflow.com/a/24176022/140800
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


class ServerspecHandler(object):

    def __init__(self):
        pass


    def verify_vms(self):

        if 'serverspec_commands' in self.config:
            cmds = [cmd.split() for cmd in self.config['serverspec_commands']]

        else:
            test_suites = self.parse_playbook()
            cmds = [["bundle", "exec", "rake", "serverspec:{}".format(suite)] for suite in test_suites]
  
        try:
            # Change directories if necessary
            if 'serverspec_base_directory' in self.config:
                with cd(self.config['serverspec_base_directory']):
                    for cmd in cmds:
                        subprocess.check_call(cmd)
            else:
                for cmd in cmds:
                    subprocess.check_call(cmd)
        except subprocess.CalledProcessError:
            raise
        finally:
            if self.args["--destroy"] == "always":
                    self.destroy_vms(self, self.args)

