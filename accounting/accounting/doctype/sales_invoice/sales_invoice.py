# Copyright (c) 2021, ruthra and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate
from frappe.model.document import Document

class SalesInvoice(Document):
        @frappe.whitelist()
        def get_tax_rate(self, item):
                item = frappe.get_doc('Items', item)
                category = frappe.get_doc('Category', item.category)
                return { 'taxrate': category.tax_rate }

        def validate(self):
                if len(self.items) == 0:
                        frappe.throw(f'Please select atleast one item')

                # make sure we have sufficient stock
                for x in self.items:
                        if x.quantity == 0:
                                frappe.throw(f'Quantity cannot be zero')

                        item_doc = frappe.get_doc('Items', x.item)
                        if item_doc.quantity < x.quantity:
                                frappe.throw(f'Only {item_doc.quantity} left in stock for Item:\'{x.item}\'')
                                

        def debit_receiver(self, reverse = False):
                gl_entry = frappe.new_doc('General Ledger')
                gl_entry.posting_date = getdate()
                gl_entry.account = 'Sales'
                if not reverse:
                        gl_entry.debit = self.total_amount
                        gl_entry.credit = 0
                else:
                        gl_entry.debit = 0
                        gl_entry.credit = self.total_amount
                gl_entry.transaction_type = 'Sales Invoice'
                gl_entry.transaction_no  =   self.name
                gl_entry.insert()
                
        def credit_giver(self, reverse = False):
                gl_entry = frappe.new_doc('General Ledger')
                gl_entry.posting_date = getdate()
                gl_entry.account = 'Debtors'
                if not reverse:
                        gl_entry.debit = 0
                        gl_entry.credit = self.total_amount
                else:
                        gl_entry.debit = self.total_amount
                        gl_entry.credit = 0
                gl_entry.transaction_type = 'Sales Invoice'
                gl_entry.transaction_no  =   self.name
                gl_entry.insert()
        

        def before_save(self):
                self.status = 'Draft'

        def before_submit(self):
                self.status = 'Unpaid'

        def on_submit(self):
                # create ledger entries
                self.debit_receiver();
                self.credit_giver();


        def before_cancel(self):
                self.status = 'Cancelled'

        def on_cancel(self):
                # reverse ledger entries
                self.debit_receiver(reverse = True)
                self.credit_giver(reverse = True)
