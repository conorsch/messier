#!/usr/bin/env python

# command line options: test, provision, destroy, etc
# in general, Vagrant commands should be honored. Depend on Vagrant
# to manage provisioning regardless of backend. Greatly simplifies scope
# of `messier`.

import vagrant


v = vagrant.Vagrant()


def create_vms():
    available_vms = [vm for vm in v.status()]
    for vm in available_vms:
        v.up(vm_name=vm.name, no_provision=True)


if __name__ == "__main__":
    create_vms()
