# Copyright (c) 2021, ruthra and Contributors
# See license.txt

import frappe
import unittest
from accounting.accounting.doctype.test_utility import wipe_all_transaction_data

class TestJournalEntry(unittest.TestCase):
        @classmethod
        def setUpClass(self):
                wipe_all_transaction_data()
                pass


        def setUp(self):
                pass

        def test_01_journal_submit(self):
                credit_acc= 'Capital'
                debit_acc= 'Cash'
                amount = 100000

                jr_entry = frappe.get_doc(
                        {
                                'doctype': 'Journal Entry',
                                'debit': debit_acc,
                                'credit': credit_acc,
                                'amount': amount
                        }).insert()
                jr_entry.submit()

                try:
                        self.assertNotEqual(frappe.db.exists({'doctype': 'General Ledger', 'transaction_no': jr_entry.name, 'account': debit_acc, 'debit': amount, 'credit': 0}), ())
                        self.assertNotEqual(frappe.db.exists({'doctype': 'General Ledger', 'transaction_no': jr_entry.name, 'account': credit_acc, 'credit': amount, 'debit': 0}), ())
                except frappe.DoesNotExistError:
                        print('Exception occured')

        def test_02_journal_cancel(self):
                credit_acc = 'Capital'
                debit_acc = 'Cash'
                amount = 100000
                
                jr_entry = frappe.get_last_doc('Journal Entry')
                jr_entry.cancel()

                try:
                        self.assertNotEqual(frappe.db.exists({'doctype': 'General Ledger', 'transaction_no': jr_entry.name, 'account': credit_acc, 'debit': amount, 'credit': 0}), ())
                        self.assertNotEqual(frappe.db.exists({'doctype': 'General Ledger', 'transaction_no': jr_entry.name, 'account': debit_acc, 'credit': amount, 'debit': 0}), ())
                except frappe.DoesNotExistError:
                        print('Exception occured')


        def tearDown(self):
                pass

        @classmethod
        def tearDownClass(self):
                pass
