# Copyright (c) 2021, ruthra and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, nowtime
from frappe.model.document import Document

class SalesInvoice(Document):
        @frappe.whitelist()
        def get_tax_rate(self, item):
                item = frappe.get_doc('Items', item)
                category = frappe.get_doc('Category', item.category)
                return { 'taxrate': category.tax_rate }

        @frappe.whitelist()
        def calculate_tax_for_item(self, lineitem):
                """ calculate tax and total for item
                item - selected item
                quantity - in integer
                return a dictionary with net total, tax and total
                """

                res = { 'tax': 0, 'net':0, 'total': 0 }
                if lineitem != None:
                        print(lineitem)
                        item = frappe.get_doc('Items', lineitem['item'])
                        category = frappe.get_doc('Category', item.category)

                        res['net'] = item.price_per_unit * lineitem['quantity']
                        res['tax'] = res['net'] * category.tax_rate
                        res['total'] = res['net'] + res['tax']

                return res

        def calculate_tax_and_total(self):
                invoice_total = 0
                total_tax = 0
                for x in self.items:
                        item = frappe.get_doc('Items', x.item)
                        category = frappe.get_doc('Category', item.category)
                        
                        x.net_amount = x.quantity * item.price_per_unit
                        x.tax = x.net_amount * category.tax_rate
                        x.total = x.net_amount + x.tax

                        invoice_total += x.total
                        total_tax += x.tax

                self.tax = total_tax
                self.total_amount = invoice_total

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

                # calculate total on items and invoice
                self.calculate_tax_and_total()


        def debit_debtors(self, reverse = False):
                gl_entry = frappe.new_doc('General Ledger')
                gl_entry.posting_date = getdate()
                gl_entry.posting_time = nowtime()
                gl_entry.account = 'Debtors'
                if not reverse:
                        gl_entry.debit = self.total_amount
                        gl_entry.credit = 0
                else:
                        gl_entry.debit = 0
                        gl_entry.credit = self.total_amount
                gl_entry.transaction_type = 'Sales Invoice'
                gl_entry.transaction_no  =   self.name
                gl_entry.insert()

        def credit_sales(self, reverse = False):
                gl_entry = frappe.new_doc('General Ledger')
                gl_entry.posting_date = getdate()
                gl_entry.posting_time = nowtime()
                gl_entry.account = 'Sales'
                if not reverse:
                        gl_entry.debit = 0
                        gl_entry.credit = self.total_amount - self.tax
                else:
                        gl_entry.debit = self.total_amount - self.tax
                        gl_entry.credit = 0
                gl_entry.transaction_type = 'Sales Invoice'
                gl_entry.transaction_no  =   self.name
                gl_entry.insert()

        def credit_tax(self, reverse = False):
                gl_entry = frappe.new_doc('General Ledger')
                gl_entry.posting_date = getdate()
                gl_entry.posting_time = nowtime()
                gl_entry.account = 'Tax'
                if not reverse:
                        gl_entry.debit = 0
                        gl_entry.credit = self.tax
                else:
                        gl_entry.debit = self.tax
                        gl_entry.credit = 0
                gl_entry.transaction_type = 'Sales Invoice'
                gl_entry.transaction_no  =   self.name
                gl_entry.insert()

        def update_item_stock(self, invoice_cancelled = False):
                if invoice_cancelled:
                        for x in self.items:
                                itm = frappe.get_doc('Items', x.item)
                                itm.quantity += x.quantity
                                itm.save()
                else:
                        for x in self.items:
                                itm = frappe.get_doc('Items', x.item)
                                itm.quantity -= x.quantity
                                itm.save()

        def before_save(self):
                self.status = 'Draft'

        def before_submit(self):
                self.status = 'Unpaid'

        def on_submit(self):
                # create ledger entries for sales
                self.debit_debtors();
                self.credit_sales();
                self.credit_tax();
                
                # update stock
                self.update_item_stock()


        def before_cancel(self):
                self.status = 'Cancelled'

        def on_cancel(self):
                # reverse ledger entries
                self.debit_debtors(reverse = True)
                self.credit_sales(reverse = True)
                self.credit_tax(reverse = True)

                # update stock
                self.update_item_stock(invoice_cancelled = True)
