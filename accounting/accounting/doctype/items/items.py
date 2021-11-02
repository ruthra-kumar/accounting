# Copyright (c) 2021, ruthra and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe import _

class Items(WebsiteGenerator):
        website = frappe._dict(
                template = "templates/generators/items.html",
                condition_field = "published"
        )
        def get_context(self, context):
                context.item = self.as_dict()
