# Copyright (c) 2021, ruthra and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, nowtime
from frappe.model.document import Document

class JournalEntry(Document):
        def validate(self):
                if self.debit == self.credit:
                        frappe.throw(f'"Debit" and "Credit" cannot be same account')

                if self.amount == 0:
                        frappe.throw(f'Amount cannot be zero')

        def debit_from_account(self, reverse=False):

                gl_entry = frappe.new_doc("General Ledger")
                gl_entry.posting_date = getdate()
                gl_entry.posting_time = nowtime()
                gl_entry.transaction_type = "Journal Entry"
                gl_entry.transaction_no = self.name
                gl_entry.account = self.debit
                if reverse:
                        gl_entry.debit = 0
                        gl_entry.credit = self.amount
                else:
                        gl_entry.debit = self.amount
                        gl_entry.credit = 0
                gl_entry.insert()
                        

        def credit_from_account(self, reverse=False):

                gl_entry = frappe.new_doc("General Ledger")
                gl_entry.posting_date = getdate()
                gl_entry.posting_time = nowtime()
                gl_entry.transaction_type = "Journal Entry"
                gl_entry.transaction_no = self.name
                gl_entry.account = self.credit
                if reverse:
                        gl_entry.debit = self.amount
                        gl_entry.credit = 0
                else:
                        gl_entry.debit = 0
                        gl_entry.credit = self.amount

                gl_entry.insert()


        def on_submit(self):
                self.debit_from_account(reverse=False)
                self.credit_from_account(reverse=False)

        def on_cancel(self):
                # on cancellation reverse the old entries
                self.debit_from_account(reverse=True)
                self.credit_from_account(reverse=True)

