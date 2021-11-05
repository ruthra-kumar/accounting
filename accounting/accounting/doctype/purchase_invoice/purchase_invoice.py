# Copyright (c) 2021, ruthra and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, nowtime
from frappe.model.document import Document

class PurchaseInvoice(Document):
        @frappe.whitelist()
        def get_tax_rate(self, item):
                item = frappe.get_doc('Items', item)
                category = frappe.get_doc('Category', item.category)
                print(category.tax_rate)
                return { 'taxrate': category.tax_rate }

        def calculate_invoice_total(self):
                invoice_total = 0
                for x in self.items:
                        item = frappe.get_doc('Items', x.item)
                        
                        x.net_amount = x.quantity * item.price_per_unit
                        x.total = x.net_amount + x.tax
                        invoice_total += x.total

                self.total_amount = invoice_total


        def validate(self):
                if self.supplier is None:
                        frappe.throw(f'Choose a supplier')

                if len(self.items) == 0:
                        frappe.throw(f'Select atleast one item')

        def debit_purchase(self, reverse = False):
                gl_entry = frappe.new_doc('General Ledger')
                gl_entry.posting_date = getdate()
                gl_entry.posting_time = nowtime()
                gl_entry.account = 'Stocks Unpaid'
                if reverse:
                        gl_entry.debit = 0
                        gl_entry.credit = self.total_amount
                else:
                        gl_entry.debit = self.total_amount
                        gl_entry.credit = 0
                gl_entry.transaction_type = 'Purchase Invoice'
                gl_entry.transaction_no  =   self.name
                gl_entry.insert()
                
        def credit_creditors(self, reverse = False):
                gl_entry = frappe.new_doc('General Ledger')
                gl_entry.posting_date = getdate()
                gl_entry.posting_time = nowtime()
                gl_entry.account = 'Creditors'
                if reverse:
                        gl_entry.debit = self.total_amount
                        gl_entry.credit = 0
                else:
                        gl_entry.debit = 0
                        gl_entry.credit = self.total_amount
                gl_entry.transaction_type = 'Purchase Invoice'
                gl_entry.transaction_no  =   self.name
                gl_entry.insert()


        def update_item_stock(self, invoice_cancelled = False):
                if invoice_cancelled:
                        for x in self.items:
                                itm = frappe.get_doc('Items', x.item)
                                itm.quantity -= x.quantity
                                itm.save()
                else:
                        for x in self.items:
                                itm = frappe.get_doc('Items', x.item)
                                itm.quantity += x.quantity
                                itm.save()

        def before_save(self):
                self.status = 'Draft'

        def before_submit(self):
                self.status = 'Unpaid'

        def on_submit(self):
                # create ledger entries
                self.debit_purchase()
                self.credit_creditors()

                # update stock
                self.update_item_stock()


        def before_cancel(self):
                self.status = 'Cancelled'

        def on_cancel(self):
                # reverse ledger entries
                self.debit_purchase(reverse = True)
                self.credit_creditors(reverse = True)

                # update stock
                self.update_item_stock(invoice_cancelled = True)
