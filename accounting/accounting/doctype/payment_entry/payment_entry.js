// Copyright (c) 2021, ruthra and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Entry', {
    refresh: function(frm) {

	frm.set_df_property('invoice_type','read_only', true);

	if(frm.doc.type == 'Receive'){
	    frm.set_value('invoice_type','Sales Invoice');
	}
	else if(frm.doc.type == 'Pay'){
	    frm.set_value('invoice_type','Purchase Invoice');
	}
    },
    setup: function(frm){
	
	// list only unpaid or partly paid invoices
	frm.set_query('invoice_no', () => {
	    return {
		filters: {
		    status: ['in', ['Unpaid', 'Partly Paid']]
		},
	    };
	});
    },
    type(frm){

	if(frm.doc.type == 'Receive'){
	    frm.set_value('invoice_type','Sales Invoice');
	}
	else if(frm.doc.type == 'Pay'){
	    frm.set_value('invoice_type','Purchase Invoice');
	}

	//clear previously selected value
	frm.set_value('invoice_no','');
    },
    invoice_no(frm){

	if(frm.doc.invoice_no){

	    frm.call('get_invoice_outstanding', {
		invoice_type: frm.doc.invoice_type,
		invoice_no: frm.doc.invoice_no,
	    })
		.then(response => {
		    if(response.message){
			frm.set_value('amount', response.message.outstanding);
		    }
		});

	    frappe.db.get_doc('Purchase Invoice', frm.doc.invoice_no)
		.then(r => {
		    frm.set_value('amount', r.total_amount);
		});
	}
    }
});
