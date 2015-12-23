# -*- coding: utf-8 -*-
import subprocess
import vagrant


class VagrantHandler(object):

    def __init__(self):
        self.v = vagrant.Vagrant(quiet_stdout=False)


    def available_vms(self):
        possible_vms = [vm for vm in self.v.status()]
        if self.args['<vms>']:
            wanted_vms = [vm for vm in possible_vms if vm.name in self.args['<vms>']]
            possible_vms = wanted_vms
        return possible_vms


    def provision_vms(self):
        for vm in self.args['vms']:
            self.v.provision(vm_name=vm.name)


    def reload_vms(self):
        for vm in self.args['vms']:
            self.v.reload(vm_name=vm.name, provision=False)


    def destroy_vms(self):
        for vm in self.args['vms']:
            self.v.destroy(vm_name=vm.name)
            # Destroy a second time because the vagrant-digitalocean plugin
            # doesn't clean up after itself:
            # https://github.com/smdahlen/vagrant-digitalocean/issues/194
            if vm.provider == "digital_ocean":
                self.v.destroy(vm_name=vm.name)


    def create_vms(self):
        for vm in self.args['vms']:
            self.v.up(vm_name=vm.name, provider=self.args['--provider'], provision=False)


    def verify_vms(self):
        r
        try:
            for suite in self.parse_playbook(self.args):
                subprocess.check_call(["bundle", "exec", "rake", "serverspec:{}".format(suite)])
        except subprocess.CalledProcessError:
            print("Serverspec run failed.")
            raise
        finally:
            if self.args["--destroy"] == "always":
                self.destroy_vms(self, self.args)

