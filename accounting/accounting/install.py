import frappe
import accounting

def after_install():
    # create basic accounts for accounting module
    accounting.setup_accounts()
