import frappe
import accounting
import unittest
import datetime

# this class has helper functions for setup and teardown

def wipe_all_accounting_data():
    """ clear all data related to accounting module, including basic accounts"""
    doctypes = [
        'Journal Entry',
        'Payment Entry',
        'Payment Items',
        'Purchase Invoice',
        'Purchase Invoice Items',
        'Sales Invoice',
        'Sales Invoice Items',
        'General Ledger',
        'Customer',
        'Items',
        'Supplier',
        'Category',
        'Accounts',
    ]

    for x in doctypes:
        frappe.db.delete(x)

    frappe.db.commit()


def wipe_all_transaction_data():
    """ 
    clear all transaction data related to accounting module.
    this includes, sales invoice, purchase invoice, payment entry, journal entry
    """
    doctypes = [
        'Journal Entry',
        'Payment Entry',
        'Payment Items',
        'Purchase Invoice',
        'Purchase Invoice Items',
        'Sales Invoice',
        'Sales Invoice Items',
        'General Ledger',
    ]

    for x in doctypes:
        frappe.db.delete(x)

    frappe.db.commit()



def setup_test_accounts():
    """ setup basic accounts for testing """
    
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
            
def setup_customers():
    frappe.get_doc({'doctype': 'Customer', 'first_name': 'John', 'last_name': 'doe','date_of_birth': datetime.date(2001,1,1)}).save()
    frappe.get_doc({'doctype': 'Customer', 'first_name': 'Denver', 'last_name': 'Lee','date_of_birth': datetime.date(2001,2,20)}).save()
    frappe.db.commit()

def setup_suppliers():
    frappe.get_doc({'doctype': 'Supplier', 'name1': 'Local', 'address': 'Local','contact': '1232434'}).save()
    frappe.get_doc({'doctype': 'Supplier', 'name1': 'JK Supplier', 'address': 'Town Centre, Near SEZ','contact': '1324543'}).save()
    frappe.db.commit()

def setup_item_categories():
    frappe.get_doc({'doctype': 'Category', 'name1': 'Electronics', 'description': 'Includes all electronic items','tax_rate': 0.18}).save()
    frappe.db.commit()
    
def setup_items():
    category = frappe.db.exists({'doctype':'Category', 'name1':'Electronics'})

    frappe.get_doc({'doctype': 'Items', 'item_name': 'Mouse', 'description': 'Wired mouse 800 dpi','quantity': 10, 'price_per_unit': 800, 'category': category[0][0]}).save()
    frappe.get_doc({'doctype': 'Items', 'item_name': 'Mac M1', 'description': 'Apple Mac M1','quantity': 10, 'price_per_unit': 90000, 'category': category[0][0]}).save()
    frappe.get_doc({'doctype': 'Items', 'item_name': 'Usb C hub', 'description': 'Honeywell USB Hub','quantity': 10, 'price_per_unit': 4500, 'category': category[0][0]}).save()
    frappe.db.commit()
    
def prepare_accounts():
    """ clear old accounts data and setup a fresh chart of accounts for testing """
    print('Clearing Old data')
    wipe_all_accounting_data()

    setup_test_accounts()
    setup_customers()
    setup_suppliers()
    setup_item_categories()
    setup_items()

    
