// Copyright (c) 2021, ruthra and contributors
// For license information, please see license.txt

frappe.ui.form.on('Journal Entry', {
    onload: function(frm){
	frm.set_query('from_account', () => {
	    return {
		filters: {
		    is_group: false
		}
	    };
	});
	frm.set_query('to_account', () => {
	    return {
		filters: {
		    is_group: false,
		}
	    };
	});

    },    
    refresh: function(frm) {

    }
});
