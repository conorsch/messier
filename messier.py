#!/usr/bin/env python
"""Messier.

Usage:
  messier.py <command> [options] [<vms> ...]

Examples:
  messier.py create server
  messier.py converge
  messier.py verify
  messier.py test
  messier.py list
  messier.py (-h | --help)
  messier.py --version

Options:
  -h --help                Show this screen.
  --provider PROVIDER      Backend provider [default: virtualbox].
  --wait <seconds>         Time to sleep after destroying [default: 10].
  --pristine               Destroy VMs prior to run.
  --reboot                 Reboot hosts prior to running Serverspec tests.
  --destroy <strategy>     Destroy hosts <passing|always|never> after running test suite [default: passing].
  --playbook <playbook>    Path to Ansible playbook for testing [default: test/default.yml].
  --keep                   Preserve existing VMs for test run.

"""
from docopt import docopt

# command line options: test, provision, destroy, etc
# in general, Vagrant commands should be honored. Depend on Vagrant
# to manage provisioning regardless of backend. Greatly simplifies scope
# of `messier`.

import vagrant
import subprocess
import yaml


v = vagrant.Vagrant(quiet_stdout=False)


def parse_playbook(args):
    playbook = open(args['--playbook'], 'r')
    y = yaml.load(playbook)
    return [play['name'] for play in y]

def available_vms(args):
    wanted_vms = [vm for vm in v.status()]
    if args['<vms>']:
        wanted_vms = [vm for vm in wanted_vms if vm in args['<vms>']]
    return wanted_vms


def provision_vms(args):
    for vm in args['vms']:
        v.provision(vm_name=vm.name)


def reload_vms(args):
    for vm in args['vms']:
        v.reload(vm_name=vm.name, provision=False)


def destroy_vms(args):
    for vm in args['vms']:
        v.destroy(vm_name=vm.name)
        # Destroy a second time because the vagrant-digitalocean plugin
        # doesn't clean up after itself:
        # https://github.com/smdahlen/vagrant-digitalocean/issues/194
        if vm.provider == "digital_ocean":
            v.destroy(vm_name=vm.name)


def create_vms(args):
    for vm in args['vms']:
        v.up(vm_name=vm.name, provider=args['--provider'], provision=False)


def verify_vms(args):
    try:
        for suite in parse_playbook(args):
            subprocess.check_call(["bundle", "exec", "rake", "serverspec:{}".format(suite)])

    except subprocess.CalledProcessError:
        print("Serverspec run failed.")
        raise

    finally:
        if args["--destroy"] == "always":
            destroy_vms(args)


if __name__ == "__main__":
    args = docopt(__doc__, version='0.1')
    args['vms'] = available_vms(args)

    if args['<command>'] == 'create':
        create_vms(args)

    elif args['<command>'] == 'destroy':
        destroy_vms(args)

    elif args['<command>'] == 'verify':
        verify_vms(args)

    elif args['<command>'] == 'test':
        if not args['--keep']:
            destroy_vms(args)
        create_vms(args)
        provision_vms(args)
        if args['--reboot']:
            reload_vms(args)
        verify_vms(args)
        if args['--destroy'] == "passing" and \
                not args['--keep']:
            destroy_vms(args)

