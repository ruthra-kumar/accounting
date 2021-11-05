# Copyright (c) 2021, ruthra and Contributors
# See license.txt

import frappe
import unittest

class TestPurchaseInvoice(unittest.TestCase):
        @classmethod
        def setUpClass(self):
                pass

        def setUp(self):
                pass

        def test_01_purchase_invoice_submit(self):
                supplier = frappe.db.exists({'doctype': 'Supplier', 'name1': 'Local'})[0][0]
                item  = frappe.db.exists({'doctype': 'Items', 'item_name': 'Mac M1'})[0][0]
                purchase_invoice_item = frappe.get_doc({'doctype':'Purchase Invoice Items'})

                price = 80000
                purchase_invoice_item.item = item
                purchase_invoice_item.price = price

                purchase_invoice = frappe.get_doc({'doctype':'Purchase Invoice', 'supplier': supplier, 'items': [purchase_invoice_item]})
                purchase_invoice.save()
                # submit invoice
                purchase_invoice.submit()

                # check ledger postings
                self.assertNotEqual(frappe.db.exists({'doctype': 'General Ledger', 'transaction_no': purchase_invoice.name, 'account': 'Creditors', 'debit': 0, 'credit': purchase_invoice.total_amount}), ())
                self.assertNotEqual(frappe.db.exists({'doctype': 'General Ledger', 'transaction_no': purchase_invoice.name, 'account': 'Stocks Unpaid', 'debit': purchase_invoice.total_amount, 'credit': 0}), ())
                
        def test_02_purchase_invoice_cancel(self):
                purchase_invoice = frappe.get_last_doc('Purchase Invoice')
                purchase_invoice.cancel()

                # check ledger postings
                self.assertNotEqual(frappe.db.exists({'doctype': 'General Ledger', 'transaction_no': purchase_invoice.name, 'account': 'Creditors', 'debit': purchase_invoice.total_amount, 'credit': 0}), ())
                self.assertNotEqual(frappe.db.exists({'doctype': 'General Ledger', 'transaction_no': purchase_invoice.name, 'account': 'Stocks Unpaid', 'debit': 0 , 'credit': purchase_invoice.total_amount}), ())


        def tearDown(self):
                pass

        @classmethod
        def tearDownClass(self):
                pass

