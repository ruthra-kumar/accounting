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
                        'read_only': 1,
                },
                {
                        'label': 'Balance',
                        'fieldname': 'balance',
                        'fieldtype': 'Currency',
                        'read_only': 1
                }]
        data, message = [], []

        income = []
        for node in get_all_child_as_list(frappe.get_doc('Accounts', 'Income').as_dict()):
                income.append({'account': node['name'],'balance': calculate_balance_on_node(node)['balance'], 'indent': node['level']})

        data += add_total_and_padding(income,'balance','Income')

        expense = []
        for node in get_all_child_as_list(frappe.get_doc('Accounts', 'Expenses').as_dict()):
                expense.append({'account': node['name'],'balance': calculate_balance_on_node(node)['balance'], 'indent': node['level']})

        data += add_total_and_padding(expense,'balance','Expense')

        # calculate net(profit/loss)
        total_income = total_expense = 0
        for x in data:
                try:
                
                        if x['account'] == 'Total Income':
                                total_income = x['balance']
                        elif x['account'] == 'Total Expense':
                                total_expense = x['balance']
                except KeyError:
                        pass
        net = total_income - total_expense
        data += [{'account': 'Net (profit/loss)', 'balance': net}]

        chart = prepare_chart(columns, data)

        return columns, data, message, chart

def prepare_chart(columns, data):

        total_income = total_expense = 0
        for x in data:
                try:
                
                        if x['account'] == 'Total Income':
                                total_income = x['balance']
                        elif x['account'] == 'Total Expense':
                                total_expense = x['balance']
                except KeyError:
                        pass
                

        chart = {
                "data": {
                        'labels': ["2021-2022"],
                        'datasets': [
                                {
                                        "name": "Total Expense",
                                        "values": [total_expense]
                                },
                                {
                                        "name": "Total Income",
                                        "values": [total_income]
                                }
                        ]
                },
                "type": "bar",
        }
        
        return chart
