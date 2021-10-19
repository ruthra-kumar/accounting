# Copyright (c) 2021, ruthra and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PurchaseInvoice(Document):
        @frappe.whitelist()
        def get_tax_rate(self, item):
                item = frappe.get_doc('Items', item)
                category = frappe.get_doc('Category', item.category)
                print(category.tax_rate)
                return { 'taxrate': category.tax_rate }

        def validate(self):
                self.status = 'Unpaid'
