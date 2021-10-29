# Copyright (c) 2013, ruthra and contributors
# License: MIT. See LICENSE

import frappe
from accounting.accounting.doctype.accounts.utils import calculate_balance_on_node, get_all_child_as_list

def get_immediate_child(node):
        """
        Get all immediate child nodes as list
        """
        if node != None:
                children = frappe.db.get_list('Accounts',filters={'parent_accounts':node['name']}, fields=['name','type','is_group'])
                return children


def execute(filters=None):
        columns = [
                {
                        'fieldname': 'account',
                        'fieldtype': 'Data',
                        'read_only': 1
                },
                {
                        'fieldname': 'balance',
                        'fieldtype': 'Currency',
                        'read_only': 1
                }]
        data = []
        accounts = frappe.db.get_list('Accounts',filters={'name':['in',['Income','Expenses']]}, fields=['name','type','is_group'])

        for acc in accounts:
                for node in get_all_child_as_list(acc):
                        data.append({'account': node['name'],'balance': calculate_balance_on_node(node)['balance']})

        return columns, data