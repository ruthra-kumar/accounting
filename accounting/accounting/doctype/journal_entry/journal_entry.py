# Copyright (c) 2021, ruthra and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate
from frappe.model.document import Document

class JournalEntry(Document):
        def validate(self):
                if self.from_account == self.to_account:
                        frappe.throw('"From" and "to" cannot be of same accounts')

        def credit_the_giver(self, reverse = False):
                gl_entry = frappe.new_doc("General Ledger")
                gl_entry.posting_date = getdate()
                gl_entry.transaction_type = "Journal Entry"
                gl_entry.transaction_no = self.name
                gl_entry.account = self.from_account
                if not reverse:
                        gl_entry.credit = self.amount
                        gl_entry.debit = 0
                else:
                        gl_entry.credit = 0
                        gl_entry.debit = self.amount
                gl_entry.insert()


        def debit_the_receiver(self, reverse = False):
                gl_entry = frappe.new_doc("General Ledger")
                gl_entry.posting_date = getdate()
                gl_entry.transaction_type = "Journal Entry"
                gl_entry.transaction_no = self.name
                gl_entry.account = self.to_account
                if not reverse:
                        gl_entry.debit = self.amount
                        gl_entry.credit = 0
                else:
                        gl_entry.debit = 0
                        gl_entry.credit = self.amount
                gl_entry.insert()


        def on_submit(self):
                self.credit_the_giver()
                self.debit_the_receiver()

        def on_cancel(self):
                # on cancellation reverse the old entries
                self.credit_the_giver(True)
                self.debit_the_receiver(True)
