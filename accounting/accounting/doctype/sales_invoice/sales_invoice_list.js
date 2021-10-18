frappe.listview_settings['Sales Invoice'] = frappe.listview_settings['Sales Invoice'] || {};

frappe.listview_settings['Sales Invoice'].add_fields = ['total_amount'];

frappe.listview_settings['Sales Invoice'].formatters = {
    total_amount(val) {
	return val;
    }
}
