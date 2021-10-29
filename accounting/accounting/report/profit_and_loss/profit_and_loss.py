# Copyright (c) 2013, ruthra and contributors
# License: MIT. See LICENSE

import frappe
from accounting.accounting.doctype.accounts.utils import calculate_balance_on_node, get_all_child_as_list, add_total_and_padding

def execute(filters=None):
        columns = [
                {
                        'label':'Account',
                        'fieldname': 'account',
                        'fieldtype': 'Data',
                        'read_only': 1
                },
                {
                        'label': 'Balance',
                        'fieldname': 'balance',
                        'fieldtype': 'Currency',
                        'read_only': 1
                }]
        data = []

        income = []
        for node in get_all_child_as_list(frappe.get_doc('Accounts', 'Income').as_dict()):
                income.append({'account': node['name'],'balance': calculate_balance_on_node(node)['balance'], 'indent': node['level']})

        data += add_total_and_padding(income,'balance','Income')

        expense = []
        for node in get_all_child_as_list(frappe.get_doc('Accounts', 'Expenses').as_dict()):
                expense.append({'account': node['name'],'balance': calculate_balance_on_node(node)['balance'], 'indent': node['level']})

        data += add_total_and_padding(expense,'balance','Expense')

        return columns, data
