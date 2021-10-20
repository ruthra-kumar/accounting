# Copyright (c) 2021, ruthra and Contributors
# See license.txt

import frappe
import unittest

class TestJournalEntry(unittest.TestCase):
        def setUp(self):
                pass

        def test_01_ledger(self):
                self.assetEqual(1,1)

        def tearDown(self):
                pass

