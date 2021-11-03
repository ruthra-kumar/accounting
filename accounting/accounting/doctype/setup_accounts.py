import frappe
import accounting
import unittest

# setup basic accounts for testing
def setup_test_accounts():


    print('Setting up test accounts')
    accounts = [    {'doctype': 'Accounts', 'name1': 'Dummy Company', 'description': 'root node for dummy company','type': 'None' ,'is_group': 1},

                    {'doctype': 'Accounts', 'name1': 'Assets','type': 'None' ,'is_group': 1 , 'parent_accounts': 'Dummy Company'},
                    {'doctype': 'Accounts', 'name1': 'Accounts Receivable','type': 'None' ,'is_group': 1 , 'parent_accounts': 'Assets'},
                    {'doctype': 'Accounts', 'name1': 'Debtors', 'is_group': 0,'type': 'Personal' , 'parent_accounts': 'Accounts Receivable'},
                    
                    {'doctype': 'Accounts', 'name1': 'Current Assets','type': 'None' ,'is_group': 1 , 'parent_accounts': 'Assets'},
                    {'doctype': 'Accounts', 'name1': 'Cash', 'is_group': 0,'type': 'Real' , 'parent_accounts': 'Current Assets'},
                    {'doctype': 'Accounts', 'name1': 'HDFC', 'is_group': 0,'type': 'Real' , 'parent_accounts': 'Current Assets'},
                    
                    {'doctype': 'Accounts', 'name1': 'Liabilities','type': 'None' ,'is_group': 1, 'parent_accounts': 'Dummy Company'},
                    {'doctype': 'Accounts', 'name1': 'Accounts Payable','type': 'None' ,'is_group': 1 , 'parent_accounts': 'Liabilities'},
                    {'doctype': 'Accounts', 'name1': 'Creditors', 'is_group': 0,'type': 'Personal' , 'parent_accounts': 'Accounts Payable'},
                    {'doctype': 'Accounts', 'name1': 'Tax', 'is_group': 0,'type': 'Nominal' , 'parent_accounts': 'Accounts Payable'},

                    {'doctype': 'Accounts', 'name1': 'Capital', 'is_group': 0,'type': 'Personal' , 'parent_accounts': 'Liabilities'},

                    {'doctype': 'Accounts', 'name1': 'Current Liabilities','type': 'None' ,'is_group': 1 , 'parent_accounts': 'Liabilities'},
                    {'doctype': 'Accounts', 'name1': 'Stocks Unpaid', 'is_group': 0,'type': 'Nominal' , 'parent_accounts': 'Current Liabilities'},
                    
                    {'doctype': 'Accounts', 'name1': 'Income','type': 'None' ,'is_group': 1, 'parent_accounts': 'Dummy Company'},
                    {'doctype': 'Accounts', 'name1': 'Sales', 'is_group': 0,'type': 'Nominal' , 'parent_accounts': 'Income'},
                    
                    {'doctype': 'Accounts', 'name1': 'Expenses','type': 'None' ,'is_group': 1, 'parent_accounts': 'Dummy Company'},
                    {'doctype': 'Accounts', 'name1': 'Purchase', 'is_group': 0,'type': 'Nominal' , 'parent_accounts': 'Expenses'}
                ]


    try:
        [frappe.get_doc(x).insert().save() for x in accounts]
    except Exception as e:
        print("Exception Occured", e)
    frappe.db.commit()
            
def prepare_accounts():
    """ clear old accounts data and setup a fresh chart of accounts for testing """
    print('Clearing Old data')
    accounting.wipe_data()

    setup_test_accounts()
    
