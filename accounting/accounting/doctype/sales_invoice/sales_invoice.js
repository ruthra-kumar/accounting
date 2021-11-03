// Copyright (c) 2021, ruthra and contributors
// For license information, please see license.txt

function calculate_invoice_total(items){
    var total = 0;
    var tax = 0;

    items.forEach(item => {
	if(item.total && Number.isNaN(Number.parseFloat(item.total)) == false){
	    total += item.total;
	    tax += item.tax;
	}
    });
    console.log(total, tax);
    return {
	'total': total,
	'tax': tax
    };
}

function calculate_item_total(frm, cdt, cdn){
    var doc = locals[cdt][cdn];
    var tax_amount = 0.0;
    var tax_rate = 0.0;
    var net_item_amount = doc.price * doc.quantity;

    frm.call('calculate_tax_for_item', {lineitem: doc})
	.then(function(response){
	    frappe.model.set_value(doc.doctype, doc.name, 'net_amount', response.message.net);
	    frappe.model.set_value(doc.doctype, doc.name, 'tax', response.message.tax);
	    frappe.model.set_value(doc.doctype, doc.name, 'total', response.message.total);

	    //calculate invoice total
	    frm.set_value('total_amount', calculate_invoice_total(frm.doc.items).total);
	    frm.set_value('tax', calculate_invoice_total(frm.doc.items).tax);

	});

}

frappe.ui.form.on('Sales Invoice', {

    validate: function(frm){
	frm.doc.items.forEach(item => {
	    if(Number.isInteger(Number.parseInt(item.quantity)) == false || Number.parseInt(item.quantity) <= 0){
		frappe.throw("Quantity should be a positive number");
	    }
	})
    },
    refresh: function(frm){
	frm.set_df_property('status','read_only', true);
	frm.set_df_property('invoice_date','read_only', true);
	frm.set_df_property('total_amount','read_only', true);

    }
});


frappe.ui.form.on('Sales Invoice Items', {
    item(frm, cdt, cdn){
	var doc = locals[cdt][cdn];
	if(doc.item && doc.quantity){
	    calculate_item_total(frm, cdt, cdn);
	}
	frm.refresh();
    },
    quantity(frm, cdt, cdn){
	var doc = locals[cdt][cdn];

	if(doc.item && doc.quantity){
	    calculate_item_total(frm, cdt, cdn);
	}
    },
    items_add(frm, cdt, cdn){
	//calculate invoice total
	frm.set_value('total_amount', calculate_invoice_total(frm.doc.items).total);
	frm.set_value('tax', calculate_invoice_total(frm.doc.items).tax);
    },
    items_remove(frm, cdt, cdn){
	//calculate invoice total
	frm.set_value('total_amount', calculate_invoice_total(frm.doc.items).total);
	frm.set_value('tax', calculate_invoice_total(frm.doc.items).tax);
    },

});
	
