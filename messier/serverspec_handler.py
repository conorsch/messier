# -*- coding: utf-8 -*-
import subprocess
from contextlib import contextmanager
import os

from .exceptions import ServerspecGemfileNotFound, AnsiblePlaybookNotFound



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
    """
    Messier utility class for managing Serverspec test suites.
    All methods are accessible via the Messier object. Call them from Messier.
    """

    def __init__(self):
        pass


    def verify_vms(self):
        """
        Run Serverspec tests suites. Accepts options `serverspec_commands`
        and `serverspec_base_directory` from the .messier config file.
        """

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
        except subprocess.CalledProcessError as e:
            if e.returncode == 10:
                raise ServerspecGemfileNotFound()
            else:
                raise


    def parse_playbook(self):
        """
        Read testing playbook and return a list of `name` attributes for each task.
        This mirrors how `ansible_spec` determines Serverspec test runs.
        """
        try:
            playbook = open(self.playbook, 'r')
        except IOError:
            raise AnsiblePlaybookNotFound
        y = yaml.load(playbook)
        return [play['name'] for play in y]
