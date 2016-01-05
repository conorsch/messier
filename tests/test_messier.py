#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_messier
----------------------------------

Tests for `messier` module.
"""

import unittest
import os
import tempfile
import yaml
import hashlib
import subprocess
import shlex

from messier import messier
from messier.serverspec_handler import cd

from messier.exceptions import VagrantfileNotFound

class TestMessier(unittest.TestCase):

    def setUp(self):
        self.messier = messier.Messier()

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    @unittest.skip("Not sure whether missing Vagrantfile should throw an error.")
    def test_empty_config(self):
        """
        Create a Messier object with no config and ensure config is empty.
        """
        temp_dir = tempfile.mkdtemp()
        with cd(temp_dir):
            m = messier.Messier()
        self.assertEqual(m.config, {})

    def test_empty_config_raises_exception(self):
        """
        Create a Messier object with no config and ensure config is empty.
        """
        temp_dir = tempfile.mkdtemp()
        with self.assertRaises(VagrantfileNotFound):
            with cd(temp_dir):
                m = messier.Messier()

    def test_custom_config(self, content=None):
        """
        Create a Messier object with a custom config file and validate the config matches.
        """
        desired_boxes = ['ubuntu/trusty64', 'ubuntu/vivid64', 'debian/jessie64']
        content = dict(vagrant_boxes=desired_boxes)
        config_path = tempfile.mktemp()
        with open(config_path, 'w') as f:
            f.write(yaml.dump(content, default_flow_style=True))
        m = messier.Messier(config_file=config_path)
        assert os.path.exists(config_path)
        for box in desired_boxes:
            assert box in m.config['vagrant_boxes']

    def test_list_vms(self, content=None):
        """
        Ensure named VM in Vagrantfile is returned by `messier list`.
        """
        # Uses tests directory?
        with cd(os.path.abspath(os.path.curdir)):
            m = messier.Messier()
            for vm in ("client", "server"):
              assert vm in [vm.name for vm in m.vms]


    @unittest.skip("`init` command not yet supported")
    def test_init_creates_vagrantfile_if_none(self):
        """
        Create a new Messier project with a Vagrantfile.
        """
        temp_dir = tempfile.mkdtemp()
        assert not os.path.exists(os.path.join(temp_dir, 'Vagrantfile'))
        with cd(temp_dir):
            m = messier.Messier()
        assert os.path.exists(os.path.join(temp_dir, 'Vagrantfile'))

    @unittest.skip("`init` command not yet supported")
    def test_init_does_not_clobber_vagrantfile(self):
        """
        Create a new Messier project and refuse to overwrite preexisting Vagrantfile.
        """
        temp_dir = tempfile.mkdtemp()
        vagrantfile = tempfile.mktemp(dir=temp_dir)
        assert os.path.exists(os.path.join(temp_dir, 'Vagrantfile'))
        original_checksum = hashlib.sha256(vagrantfile).hexdigest()
        with cd(temp_dir):
            m = messier.Messier()
        assert os.path.exists(os.path.join(temp_dir, 'Vagrantfile'))
        new_checksum = hashlib.sha256(vagrantfile).hexdigest()
        assert new_checksum == original_checksum

    def test_create_vms(self):
        """
        Create VMs from existing Vagrantfile and ensure they are running.
        """
        m = messier.Messier()
        m.create_vms()
        for vm in m.vms:
            assert vm.state == "running"

    def test_reload_vms(self):
        """
        Reboot VMs and check that uptime decreased.
        """
        m = messier.Messier()
        m.create_vms()
        original_uptimes = {}

        def get_uptime(vm):
            """
            Return uptime in seconds for vm
            """
            # Hideous one-liner, but it works.
            cmd = """vagrant ssh {} --command \"cut -d' ' -f 1 /proc/uptime\" """.format(vm.name)
            cmd = shlex.split(cmd)
            return subprocess.check_output(cmd, stderr=open('/dev/null', 'w'))

        for vm in m.vms:
            uptime = get_uptime(vm)
            original_uptimes[vm.name] = uptime

        new_uptimes = {}
        for vm in m.vms:
            m.v.reload(vm_name=vm.name)
            new_uptime = get_uptime(vm)
            new_uptimes[vm.name] = new_uptime

        for k, v in original_uptimes.items():
            assert new_uptimes[k] < v

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
