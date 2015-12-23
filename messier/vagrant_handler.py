# -*- coding: utf-8 -*-
import vagrant


class VagrantHandler(object):
    """
    Messier utility class for managing Vagrant VMs.
    All methods are accessible via the Messier object. Call them from Messier.
    """

    def __init__(self):
        """
        Initialize Vagrant handler via self.v. Uses python-vagrant.
        """
        self.v = vagrant.Vagrant()


    def available_vms(self):
        """
        List all VMs regardless of state, filtering if requested via the <vms>
        parameter provider by the CLI.
        """
        possible_vms = [vm for vm in self.v.status()]
        if self.args['<vms>']:
            wanted_vms = [vm for vm in possible_vms if vm.name in self.args['<vms>']]
            possible_vms = wanted_vms
        return possible_vms


    def provision_vms(self):
        """
        Runs provisioner (defaults to Ansible) against target VMs.
        Vagrant handler will print provisioner output to STDOUT during
        provisioner run, and resilence output after running.
        """
        # Renable stdout to watch provisioner output
        self.v.out_cm = vagrant.stdout_cm

        # In multi-machine environments, the Ansible provisioner for Vagrant
        # expects only a single target, allowing Ansible to handle sorting out
        # the correct host list via limit=all.
        if 'provision_target' in self.config:
            self.v.provision(vm_name=self.config['provision_target'])
        else:
            for vm in self.args['vms']:
                self.v.provision(vm_name=vm.name)

        # Resilence stdout to noisy Vagrant commands don't pollute output.
        self.v.out_cm = vagrant.devnull_cm


    def reload_vms(self):
        """
        Reboot target VMs. Operates on all available VMs if none are specified.
        """
        for vm in self.args['vms']:
            self.v.reload(vm_name=vm.name, provision=False)


    def destroy_vms(self):
        """
        Destroy target VMs. Operates on all available VMs if none are specified.
        """
        for vm in self.args['vms']:
            self.v.destroy(vm_name=vm.name)
            # Destroy a second time because the vagrant-digitalocean plugin
            # doesn't clean up after itself:
            # https://github.com/smdahlen/vagrant-digitalocean/issues/194
            if vm.provider == "digital_ocean":
                self.v.destroy(vm_name=vm.name)


    def create_vms(self):
        """
        Create target VMs, but do not provision. Operates on all available 
        VMs if none are specified.
        """
        for vm in self.args['vms']:
            self.v.up(vm_name=vm.name, provider=self.args['--provider'], provision=False)


