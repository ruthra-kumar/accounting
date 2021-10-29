# Copyright (c) 2021, ruthra and Contributors
# See license.txt

import frappe
import unittest

# def setup_accounts(self):
#         try:
#                 frappe.get_doc('Accounts', 'dummy')
#         except frappe.DoesNotExistError:
#                 frappe.get_doc({'doctype': 'Accounts', 'name1': 'dummy', 'description': 'dummy company root node', 'is_group': 1}).insert().save()
#         else:
#                 frappe.db.delete('Accounts')
#                 frappe.get_doc({'doctype': 'Accounts', 'name1': 'dummy', 'description': 'dummy company root node', 'is_group': 1}).insert().save()

#         accounts = ['Sales', 'Purchase', 'Payments', 'Debtors', 'Creditors', 'HDFC']
#         list(map(lambda acc: frappe.get_doc({'doctype': 'Accounts', 'name1': acc, 'parent_accounts': 'dummy' }).insert().save(), accounts))

# def clear_accounts(self): 
#         frappe.db.delete('Accounts')       

class TestJournalEntry(unittest.TestCase):
        @classmethod
        def setUpClass(self):
                # setup_accounts(self)
                pass


        def setUp(self):
                pass

        def test_01_journal_submit(self):
                from_acc = 'Debtors'
                to_acc = 'Sales'
                amount = 1000
                gl_entries = None

                jr_entry = frappe.get_doc(
                        {
                                'doctype': 'Journal Entry',
                                'debit': from_acc,
                                'credit': to_acc,
                                'amount': amount
                        }).insert()
                jr_entry.submit()

                try:
                        self.assertIsNotNone(frappe.db.exists({'doctype': 'General Ledger','transaction_type': 'Journal Entry', 'transaction_no': jr_entry.name, 'account': from_acc, 'debit': amount}))
                        self.assertIsNotNone(frappe.db.exists({'doctype': 'General Ledger','transaction_type': 'Journal Entry', 'transaction_no': jr_entry.name, 'account': to_acc, 'credit': amount}))
                except frappe.DoesNotExistError:
                        self.assertIsNotNone(gl_entries)

        def test_02_journal_cancel(self):
                from_acc = 'Debtors'
                to_acc = 'Sales'
                amount = 1000
                gl_entries = None

                
                jr_entry = frappe.get_last_doc('Journal Entry',
                                               filters={
                                                       'debit': from_acc,
                                                       'credit': to_acc,
                                               })
                jr_entry.cancel()

                try:
                        self.assertIsNotNone(frappe.db.exists({'doctype': 'General Ledger','transaction_type': 'Journal Entry', 'transaction_no': jr_entry.name, 'account': from_acc, 'credit': amount}))
                        self.assertIsNotNone(frappe.db.exists({'doctype': 'General Ledger','transaction_type': 'Journal Entry', 'transaction_no': jr_entry.name, 'account': to_acc, 'debit': amount}))
                except frappe.DoesNotExistError:
                        self.assertIsNotNone(gl_entries)


        def tearDown(self):
                pass

        @classmethod
        def tearDownClass(self):
                # clear_accounts(self)
                pass

