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

from messier import messier
from messier.serverspec_handler import cd


class TestMessier(unittest.TestCase):

    def setUp(self):
        self.messier = messier.Messier()

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_empty_config(self):
        """
        Create a Messier object with no config and ensure config is empty.
        """
        temp_dir = tempfile.mkdtemp()
        with cd(temp_dir):
            m = messier.Messier()
        self.assertEqual(m.config, {})

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


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
