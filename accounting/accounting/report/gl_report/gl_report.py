# Copyright (c) 2013, ruthra and contributors
# License: MIT. See LICENSE

import frappe

from accounting.accounting.doctype.accounts.utils import get_all_child_as_list

def execute(filters=None):
        columns = [
                {
                        "default": "Today",
                        "fieldname": "posting_date",
                        "fieldtype": "Date",
                        "in_list_view": 1,
                        "label": "Posting Date",
                        "read_only": 1,
                        "reqd": 1
                },
                {
                        "fieldname": "posting_time",
                        "fieldtype": "Time",
                        "label": "Posting Time",
                        "read_only": 1,
                        "reqd": 1
                },
                {
                        "fieldname": "account",
                        "fieldtype": "Link",
                        "in_list_view": 1,
                        "label": "Account",
                        "options": "Accounts",
                        "reqd": 1
                },
                {
                        "fieldname": "debit",
                        "fieldtype": "Currency",
                        "label": "Debit"
                },
                {
                        "fieldname": "credit",
                        "fieldtype": "Currency",
                        "label": "Credit"
                },
                {
                        "fieldname": "balance",
                        "fieldtype": "Currency",
                        "label": "Balance"
                },
                {
                        "fieldname": "transaction_type",
                        "fieldtype": "Data",
                        "label": "Transaction Type"
                },
                {
                        "fieldname": "transaction_no",
                        "fieldtype": "Data",
                        "label": "Transaction No"
                }]

        gl_entries = []
   
        try:
                filter_node = filters['account']
                node = frappe.get_doc('Accounts', filter_node)
                acc_list = []
                if node.is_group:
                        acc_list = get_all_child_as_list(node.as_dict())

                        # get leaf nodes
                        acc_list = list(filter(lambda x: not x['is_group'],acc_list))

                        # get accounts names
                        acc_name = [x['name'] for x in acc_list]

                        print("Accout List:",acc_list)
                        gl_entries = frappe.db.get_list('General Ledger', filters={'account': ['in', acc_name]}, fields = ['posting_date', 'posting_time','account', 'debit', 'credit', 'transaction_no', 'transaction_type'], order_by="posting_date,posting_time")

                else:
                        gl_entries = frappe.db.get_list('General Ledger', filters={'account': node.name}, fields = ['posting_date', 'posting_time','account', 'debit', 'credit', 'transaction_no', 'transaction_type'], order_by="posting_date,posting_time")
                
        except KeyError:
                gl_entries = frappe.get_all('General Ledger', fields = ['posting_date', 'posting_time','account', 'debit', 'credit', 'transaction_no', 'transaction_type'], order_by="posting_date,posting_time")
        
        balance = 0
        total_debit = 0
        total_credit = 0
        for x in gl_entries:
                total_debit += x['debit']
                total_credit += x['credit']
                x['balance'] = balance = balance + ( x['debit'] - x['credit'] )
                

        # add opening 
        gl_entries = [{'account': 'Opening', 'credit': 0, 'debit': 0, 'balance': 0}] + gl_entries

        #add total
        gl_entries = gl_entries + [{'account': 'Total', 'credit': total_credit, 'debit': total_debit, 'balance': 0}]


        data = gl_entries
        return columns, data
