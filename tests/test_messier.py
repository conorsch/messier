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

from messier import messier


class TestMessier(unittest.TestCase):

    def setUp(self):
        self.messier = messier.Messier()

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_empty_config(self):
        """
        Create a .messier config file and validate its contents.
        """
        config = self.messier.config()
        self.assertEqual(config, {})

    def test_empty_config(self):
        """
        Create a .messier config file and validate its contents.
        """
        config = self.messier.config
        self.assertEqual(config, {})

    def test_custom_config(self, content=None):
        content = """
        ---
        vagrant_boxes:
          - ubuntu/trusty64
          - ubuntu/vivid64
        """.strip()
        config, config_path  = tempfile.mkstemp(text=True)

        with open(config_path, 'w') as f:
            f.write(content)
        m = messier.Messier(config_file=config_path)
        desired_boxes = ['ubuntu/trusty64', 'ubuntu/vivid64']
        for box in desired_boxes:
            assert box in m.config['vagrant_boxes']
        assert os.path.exists(".messier")


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
