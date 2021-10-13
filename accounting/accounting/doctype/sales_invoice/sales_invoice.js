// Copyright (c) 2021, ruthra and contributors
// For license information, please see license.txt

function calculate_invoice_total(items){
    var total = 0;

    items.forEach(item => {
	if(item.total && Number.isNaN(Number.parseFloat(item.total)) == false){
	    total += item.total;
	}
    });

    return total;
}

frappe.ui.form.on('Sales Invoice', {
    // refresh: function(frm) {

    // }

    validate: function(frm){
	frm.doc.items.forEach(item => {
	    if(Number.isInteger(Number.parseInt(item.quantity)) == false || Number.parseInt(item.quantity) <= 0){
		frappe.throw("Quantity should be a positive number");
	    }
	})
    }
});


frappe.ui.form.on('Sales Invoice Items', {
    item(frm, cdt, cdn){
	var doc = locals[cdt][cdn];

	//calculate price on item
	if(doc.item && doc.quantity){
	    frappe.model.set_value(doc.doctype, doc.name, 'total', doc.price * doc.quantity);
	}

	//calculate invoice total
	frm.set_value('total_amount', calculate_invoice_total(frm.doc.items));
    },
    quantity(frm, cdt, cdn){
	var doc = locals[cdt][cdn];

	//calculate price on item
	if(doc.item && doc.quantity){
	    frappe.model.set_value(doc.doctype, doc.name, 'total', doc.price * doc.quantity);
	}

	//calculate invoice total
	frm.set_value('total_amount', calculate_invoice_total(frm.doc.items));
    },
    items_add(frm, cdt, cdn){
	//calculate invoice total
	frm.set_value('total_amount', calculate_invoice_total(frm.doc.items));
    },
    items_remove(frm, cdt, cdn){
	console.log("row removed");
	//calculate invoice total
	frm.set_value('total_amount', calculate_invoice_total(frm.doc.items));
    },

});
	
