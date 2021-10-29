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

function calculate_item_total(frm, cdt, cdn){
    var doc = locals[cdt][cdn];
    var tax_amount = 0.0;
    var tax_rate = 0.0;
    var net_item_amount = doc.price * doc.quantity;


    frm.call('get_tax_rate', {item: doc.item})
	.then(function(response){
	    //get tax
	    tax_rate = response.message.taxrate;
	    tax_amount = net_item_amount * tax_rate;


	    //calculate price on item
	    if(doc.item && doc.quantity){
		frappe.model.set_value(doc.doctype, doc.name, 'net_amount', net_item_amount);
		frappe.model.set_value(doc.doctype, doc.name, 'tax', tax_amount);
		frappe.model.set_value(doc.doctype, doc.name, 'total', net_item_amount + tax_amount);
	    }

	    //calculate invoice total
	    frm.set_value('total_amount', calculate_invoice_total(frm.doc.items));
	});
}

frappe.ui.form.on('Sales Invoice', {

    // onload: function(frm){
    // 	if(frm.doc.items){
    // 	    frm.set_value('items',[]);
    // 	    // frappe.new_doc('Sales Invoice Items')
    // 	    // 	.then( response => {
    // 	    // 	    frm.doc.items.push(r.message);
    // 	    // 	});
    // 	}
    // },
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
    },
    quantity(frm, cdt, cdn){
	var doc = locals[cdt][cdn];

	if(doc.item && doc.quantity){
	    calculate_item_total(frm, cdt, cdn);
	}
    },
    items_add(frm, cdt, cdn){
	//calculate invoice total
	frm.set_value('total_amount', calculate_invoice_total(frm.doc.items));
    },
    items_remove(frm, cdt, cdn){
	//calculate invoice total
	frm.set_value('total_amount', calculate_invoice_total(frm.doc.items));
    },

});
	
