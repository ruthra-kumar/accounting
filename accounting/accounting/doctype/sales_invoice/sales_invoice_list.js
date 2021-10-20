frappe.listview_settings['Sales Invoice'] = frappe.listview_settings['Sales Invoice'] || {};

frappe.listview_settings['Sales Invoice'].add_fields = ['total_amount', 'status'];

frappe.listview_settings['Sales Invoice'].formatters = {
    total_amount(val) {
	return val;
    },
    status(val) {
	return val;
    }
}
