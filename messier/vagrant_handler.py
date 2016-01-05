# -*- coding: utf-8 -*-
import vagrant
from subprocess import CalledProcessError

from .exceptions import VagrantfileNotFound


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
        try:
            possible_vms = [vm for vm in self.v.status()]
        except CalledProcessError, e:
            # TODO: Exception handling here assumes Vagrantfile is missing.
            # Vagrant seems to return 1 for many different errors, and finding
            # documentation for specific return codes has proven difficult.
            raise VagrantfileNotFound

        if self.vms:
            wanted_vms = [vm for vm in possible_vms if vm.name in self.vms]
            possible_vms = wanted_vms
        else:
            self.vms = possible_vms
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
            for vm in self.vms:
                self.v.provision(vm_name=vm.name)

        # Resilence stdout to noisy Vagrant commands don't pollute output.
        self.v.out_cm = vagrant.devnull_cm


    def reload_vms(self):
        """
        Reboot target VMs. Operates on all available VMs if none are specified.
        """
        for vm in self.vms:
            self.v.reload(vm_name=vm.name, provision=False)


    def destroy_vms(self):
        """
        Destroy target VMs. Operates on all available VMs if none are specified.
        """
        for vm in self.vms:
            # Vagrant will return 1 if VM to be destroyed does not exist.
            if vm.state != "not_created":
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
        for vm in self.vms:
            self.v.up(vm_name=vm.name, provider=self.provider, provision=False)

