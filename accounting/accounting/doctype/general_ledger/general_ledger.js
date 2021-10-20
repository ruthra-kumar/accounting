// Copyright (c) 2021, ruthra and contributors
// For license information, please see license.txt

frappe.ui.form.on('General Ledger', {
    setup: function(frm) {
	frm.doc.posting_time = frappe.datetime.now_time();
    },
    refresh: function(frm) {
	frm.doc.posting_time = frappe.datetime.now_time();
    }
});
