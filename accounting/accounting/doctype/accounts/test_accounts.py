# Copyright (c) 2021, ruthra and Contributors
# See license.txt

import frappe
import unittest
from accounting.accounting.doctype.accounts.utils import calculate_balance_on_node
from accounting.accounting.doctype.test_utility import wipe_all_transaction_data

class TestAccounts(unittest.TestCase):
        def setUp(self):
                wipe_all_transaction_data()

        def test_01_accounts(self):
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

        def test_02_balance(self):
                customer = frappe.db.exists({'doctype': 'Customer', 'first_name': 'Denver'})[0][0]
                item  = frappe.db.exists({'doctype': 'Items', 'item_name': 'Mac M1'})[0][0]
                sales_invoice_item = frappe.get_doc({'doctype':'Sales Invoice Items'})


                sales_invoice_item.item = item
                sales_invoice_item.price = frappe.get_doc('Items',item).price_per_unit

                sales_invoice = frappe.get_doc({'doctype':'Sales Invoice', 'customer': customer, 'items': [sales_invoice_item]})
                sales_invoice.save()
                # submit invoice
                sales_invoice.submit()

                accounts = frappe.db.get_list('Accounts', filters={'name': ['in', ['Assets', 'Income', 'Liabilities']]}, fields=['name', 'is_group', 'type'])

                # check balance
                self.assertEqual(calculate_balance_on_node(list(filter(lambda x: x['name'] == 'Assets', accounts))[0])['balance'], 106200)
                self.assertEqual(calculate_balance_on_node(list(filter(lambda x: x['name'] == 'Income', accounts))[0])['balance'], 90000)
                self.assertEqual(calculate_balance_on_node(list(filter(lambda x: x['name'] == 'Liabilities', accounts))[0])['balance'], 16200)
