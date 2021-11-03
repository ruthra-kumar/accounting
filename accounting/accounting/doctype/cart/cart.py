# Copyright (c) 2021, ruthra and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Cart(WebsiteGenerator):
        @frappe.whitelist()
        def calculate_total(self):
                print('point reached')

        def validate(self):
                # throw if cart is empty
                if self.items == []:
                        frappe.throw('Select atleast one item')
                
