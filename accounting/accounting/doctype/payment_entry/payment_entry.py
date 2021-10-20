# Copyright (c) 2021, ruthra and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, nowtime
from frappe.model.document import Document

class PaymentEntry(Document):
        # calculate outstanding amount for invoice
        @frappe.whitelist()
        def get_invoice_outstanding(self, invoice_type, invoice_no):
                total_active = 0
                active_payments = frappe.db.get_list('Payment Entry', fields=['name','amount'], filters={'invoice_no': invoice_no, 'docstatus': '1'})
                invoice = frappe.get_doc(invoice_type, invoice_no)
                for x in active_payments:
                        total_active += x.amount

                return { 'outstanding': float(invoice.total_amount - total_active) }


        def update_invoice_status(self, entry_creation=True):
                outstanding_amount = self.get_invoice_outstanding(self.invoice_type, self.invoice_no)['outstanding']
                invoice = frappe.get_doc(self.invoice_type, self.invoice_no)

               # When a new payment entry is created
                if entry_creation:
                        if 0 == outstanding_amount:
                                invoice.db_set('status', 'Paid')
                        elif outstanding_amount > 0:
                                invoice.db_set('status', 'Partly Paid')
                
                # when a payment entry is cancelled
                else:
                        if outstanding_amount > 0 and outstanding_amount == invoice.total_amount:
                                invoice.db_set('status', 'Unpaid')
                        elif outstanding_amount < invoice.total_amount:
                                invoice.db_set('status', 'Partly Paid')
                        
                invoice.save()

        def on_submit(self):
                if self.invoice_no is not None:

                        gl_entry = frappe.new_doc('General Ledger')
                        gl_entry.posting_date = getdate()
                        gl_entry.posting_time = nowtime()
                        gl_entry.transaction_type = 'Payment Entry'
                        gl_entry.transaction_no = self.name
                        gl_entry.account = 'Debtors'
                        gl_entry.credit = self.amount
                        gl_entry.debit = 0
                        gl_entry.insert()

                        # Debit Sales
                        gl_entry = frappe.new_doc('General Ledger')
                        gl_entry.posting_date = getdate()
                        gl_entry.posting_time = nowtime()
                        gl_entry.transaction_type = 'Payment Entry'
                        gl_entry.transaction_no = self.name
                        gl_entry.account = 'Sales'
                        gl_entry.credit = 0
                        gl_entry.debit = self.amount
                        gl_entry.insert()

                        self.update_invoice_status()

        def on_cancel(self):
                # Reverse General Ledger posting
                gl_entry = frappe.new_doc('General Ledger')
                gl_entry.posting_date = getdate()
                gl_entry.posting_time = nowtime()
                gl_entry.transaction_type = 'Payment Entry'
                gl_entry.transaction_no = self.name
                gl_entry.account = 'Sales'
                gl_entry.credit = self.amount
                gl_entry.debit = 0
                gl_entry.insert()

                gl_entry = frappe.new_doc('General Ledger')
                gl_entry.posting_date = getdate()
                gl_entry.posting_time = nowtime()
                gl_entry.transaction_type = 'Payment Entry'
                gl_entry.transaction_no = self.name
                gl_entry.account = 'Debtors'
                gl_entry.credit = 0
                gl_entry.debit = self.amount
                gl_entry.insert()

                self.update_invoice_status(entry_creation=False)


