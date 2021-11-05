# Copyright (c) 2021, ruthra and Contributors
# See license.txt

import frappe
import unittest

class TestSalesInvoice(unittest.TestCase):
        @classmethod
        def setUpClass(self):
                pass

        def setUp(self):
                pass

        def test_01_sales_invoice_submit(self):
                customer = frappe.db.exists({'doctype': 'Customer', 'first_name': 'Denver'})[0][0]
                item  = frappe.db.exists({'doctype': 'Items', 'item_name': 'Mac M1'})[0][0]
                sales_invoice_item = frappe.get_doc({'doctype':'Sales Invoice Items'})


                sales_invoice_item.item = item
                sales_invoice_item.price = frappe.get_doc('Items',item).price_per_unit

                sales_invoice = frappe.get_doc({'doctype':'Sales Invoice', 'customer': customer, 'items': [sales_invoice_item]})
                sales_invoice.save()
                # submit invoice
                sales_invoice.submit()

                # check ledger postings
                self.assertNotEqual(frappe.db.exists({'doctype': 'General Ledger', 'transaction_no': sales_invoice.name, 'account': 'Debtors', 'debit': sales_invoice.total_amount, 'credit': 0}), ())
                self.assertNotEqual(frappe.db.exists({'doctype': 'General Ledger', 'transaction_no': sales_invoice.name, 'account': 'Sales', 'debit': 0, 'credit': sales_invoice.total_amount-sales_invoice.tax}), ())
                self.assertNotEqual(frappe.db.exists({'doctype': 'General Ledger', 'transaction_no': sales_invoice.name, 'account': 'Tax', 'debit': 0, 'credit': sales_invoice.tax}), ())
                
        def test_02_sales_invoice_cancel(self):
                sales_invoice = frappe.get_last_doc('Sales Invoice')
                sales_invoice.cancel()

                # check ledger postings
                self.assertNotEqual(frappe.db.exists({'doctype': 'General Ledger', 'transaction_no': sales_invoice.name, 'account': 'Debtors', 'debit': 0, 'credit': sales_invoice.total_amount }), ())
                self.assertNotEqual(frappe.db.exists({'doctype': 'General Ledger', 'transaction_no': sales_invoice.name, 'account': 'Sales', 'debit':  sales_invoice.total_amount-sales_invoice.tax, 'credit': 0}), ())
                self.assertNotEqual(frappe.db.exists({'doctype': 'General Ledger', 'transaction_no': sales_invoice.name, 'account': 'Tax', 'debit': sales_invoice.tax, 'credit': 0}), ())

        def tearDown(self):
                pass

        @classmethod
        def tearDownClass(self):
                pass
