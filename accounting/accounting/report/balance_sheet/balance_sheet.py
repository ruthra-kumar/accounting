# Copyright (c) 2013, ruthra and contributors
# License: MIT. See LICENSE

import frappe
from accounting.accounting.doctype.accounts.utils import calculate_balance_on_node, get_all_child_as_list, add_total_and_padding

def execute(filters=None):
        columns = [
                {
                        'label': 'Account',
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
        assets = []
        for node in get_all_child_as_list(frappe.get_doc('Accounts', 'Assets').as_dict()):
                assets.append({'account': node['name'],'balance': calculate_balance_on_node(node)['balance'], 'indent': node['level']})

        data += add_total_and_padding(assets,'balance','Assets')

        liabilities = []
        for node in get_all_child_as_list(frappe.get_doc('Accounts', 'Liabilities').as_dict()):
                liabilities.append({'account': node['name'],'balance': calculate_balance_on_node(node)['balance'], 'indent': node['level']})

        data += add_total_and_padding(liabilities,'balance','Liabilities')

        return columns, data
