#!/usr/bin/env python

# command line options: test, provision, destroy, etc
# in general, Vagrant commands should be honored. Depend on Vagrant
# to manage provisioning regardless of backend. Greatly simplifies scope
# of `messier`.

import vagrant


v = vagrant.Vagrant()

testing_vms = ['server', 'client']

for vm in testing_vms:
    v.up(vm_name=vm, no_provision=True)

