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
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_init(self):
        """
        Create a .messier config file and validate its contents.
        """
        messier.config.init()
        assert os.path.existS(".messier")






if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
