# -*- coding: utf-8 -*-
class VagrantHandler(object):
    def __init__(self):
        self.v = vagrant.Vagrant(quiet_stdout=False)


    def parse_playbook(self, args):
        playbook = open(args['--playbook'], 'r')
        y = yaml.load(playbook)
        return [play['name'] for play in y]


    def available_vms(self, args):
        possible_vms = [vm for vm in self.v.status()]
        if args['<vms>']:
            wanted_vms = [vm for vm in possible_vms if vm.name in args['<vms>']]
            possible_vms = wanted_vms
        return possible_vms


    def provision_vms(self, args):
        for vm in args['vms']:
            self.v.provision(vm_name=vm.name)


    def reload_vms(self, args):
        for vm in args['vms']:
            self.v.reload(vm_name=vm.name, provision=False)


    def destroy_vms(self, args):
        for vm in args['vms']:
            self.v.destroy(vm_name=vm.name)
            # Destroy a second time because the vagrant-digitalocean plugin
            # doesn't clean up after itself:
            # https://github.com/smdahlen/vagrant-digitalocean/issues/194
            if vm.provider == "digital_ocean":
                self.v.destroy(vm_name=vm.name)


    def create_vms(self, args):
        for vm in args['vms']:
            self.v.up(vm_name=vm.name, provider=args['--provider'], provision=False)


    def verify_vms(self, args):
        try:
            for suite in self.parse_playbook(args):
                subprocess.check_call(["bundle", "exec", "rake", "serverspec:{}".format(suite)])
        except subprocess.CalledProcessError:
            print("Serverspec run failed.")
            raise
        finally:
            if args["--destroy"] == "always":
                self.destroy_vms(self, args)

