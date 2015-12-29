#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_messier
----------------------------------

Tests for `messier` module.
"""

import unittest
import os

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


    def test_custom_config(self):
        pass
        assert os.path.exists(".messier")






if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
