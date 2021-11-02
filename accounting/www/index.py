import frappe

def get_context(context):
    context.hey = 'Hello'
    for key, values in frappe.session.items():
        print(key, values)

    print(frappe)


