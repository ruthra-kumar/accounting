
__version__ = '0.0.1'

import frappe
def delete_records(rec):
    if rec.docstatus == 1:
        print(f'{rec.name} cancelling')
        rec.cancel()
        print(f'{rec.name} deleted')
        rec.delete()

    elif rec.docstatus == 2:
        print(f'{rec.name} deleted')
        rec.delete()

    elif rec.docstatus == 0:
        print(f'{rec.name} deleted')
        rec.delete()


def wipe_data():
    doctypes = [
        'Journal Entry',
        'Payment Entry',
        'Payment Items',
        'Purchase Invoice',
        'Purchase Invoice Items',
        'Sales Invoice',
        'Sales Invoice Items',
        'General Ledger'
    ]

    # cancel existing items
    records = []

    for x in doctypes:
        for rec in frappe.db.get_list(x, fields=['name']):
            records.append(frappe.get_doc(x, rec.name))

    list(map(delete_records, records))
    frappe.db.commit()


