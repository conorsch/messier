#!/usr/bin/env python

import vagrant
import subprocess
import json


v = vagrant.Vagrant()
running_vms = [vm for vm in v.status() if vm.state == v.RUNNING]


def convert_ssh_options(ssh_config):
    ssh_option_mapping = {
        'HostName': 'ansible_ssh_host',
        'User': 'ansible_ssh_user',
        'Port': 'ansible_ssh_port',
        'IdentityFile': 'ansible_ssh_private_key_file',
    }
    ansible_options = {}
    for k, v in ssh_config.iteritems():
        if k in ssh_option_mapping.keys():
            ansible_options[ssh_option_mapping[k]] = v
    return ansible_options


inventory = {
    "vagrant": {
        "hosts": [vm.name for vm in running_vms],
    },
    "virtualbox": {
        "hosts": [vm.name for vm in running_vms if vm.provider == 'virtualbox'],
    },
    "digital_ocean": {
        "hosts": [vm.name for vm in running_vms if vm.provider == 'digital_ocean'],
    },
    "client": {
        "hosts": [vm.name for vm in running_vms if vm.name == 'client'],
    },
    "server": {
        "hosts": [vm.name for vm in running_vms if vm.name == 'server'],
    },
    "_meta": {
        "hostvars": {
            vm.name:
                convert_ssh_options(v.conf(vm_name=vm.name))
            for vm in running_vms
        }
    }
}


print(json.dumps(inventory, indent=2))
