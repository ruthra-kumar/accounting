# Copyright (c) 2021, ruthra and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PurchaseInvoice(Document):
        def validate(self):
                self.status = 'Unpaid'
