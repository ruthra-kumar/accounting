# Copyright (c) 2021, ruthra and Contributors
# See license.txt

import frappe
import unittest

class TestAccounts(unittest.TestCase):
        def test_accounts(self):
                self.assertIsNotNone(frappe.db.exists('Accounts', 'Dummy Company'))
                self.assertIsNotNone(frappe.db.exists('Accounts', 'Assets'))
                self.assertIsNotNone(frappe.db.exists('Accounts', 'Liabilities'))
                self.assertIsNotNone(frappe.db.exists('Accounts', 'Income'))
                self.assertIsNotNone(frappe.db.exists('Accounts', 'Expenses'))
                self.assertIsNotNone(frappe.db.exists('Accounts', 'Cash '))
                self.assertIsNotNone(frappe.db.exists('Accounts', 'Debtors'))
                self.assertIsNotNone(frappe.db.exists('Accounts', 'HDFC '))
                self.assertIsNotNone(frappe.db.exists('Accounts', 'Creditors'))
                self.assertIsNotNone(frappe.db.exists('Accounts', 'Tax'))
                self.assertIsNotNone(frappe.db.exists('Accounts', 'Capital'))
                self.assertIsNotNone(frappe.db.exists('Accounts', 'Purchase'))
                self.assertIsNotNone(frappe.db.exists('Accounts', 'Sales '))
