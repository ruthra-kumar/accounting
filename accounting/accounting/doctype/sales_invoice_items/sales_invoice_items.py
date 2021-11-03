# Copyright (c) 2021, ruthra and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SalesInvoiceItems(Document):
        def calculate_tax(self):
                print(self)
                
        def validate(self):
                if self.item != None and self.quantity != None:
                        calculate_tax()
                        
                

