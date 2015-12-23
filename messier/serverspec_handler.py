# -*- coding: utf-8 -*-
import subprocess


class ServerspecHandler(object):

    def __init__(self):
        pass


    def verify_vms(self):
        try:
            for suite in self.parse_playbook():
                subprocess.check_call(["bundle", "exec", "rake", "serverspec:{}".format(suite)])
        except subprocess.CalledProcessError:
            print("Serverspec run failed.")
            raise
        finally:
            if self.args["--destroy"] == "always":
                self.destroy_vms(self, self.args)


