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

frappe.ui.form.on('Purchase Invoice', {
    onload: function(frm){
	if(!frm.doc.items){
	    frm.set_value('total_amount', 0);
	}
    },
    refresh: function(frm) {
	frm.set_df_property('total_amount','read_only', true);
	frm.set_df_property('status','read_only', true);
	frm.set_df_property('invoice_date','read_only', true);
    },
    validate: function(frm){
	frm.doc.items.forEach(item => {
	    if(Number.isInteger(Number.parseInt(item.quantity)) == false || Number.parseInt(item.quantity) <= 0){
		frappe.throw("Quantity should be a positive number");
	    }
	})
    }
});


frappe.ui.form.on('Purchase Invoice Items', {
    item(frm, cdt, cdn){
	var doc = locals[cdt][cdn];
	if(doc.item && doc.quantity && doc.price){
	    calculate_item_total(frm, cdt, cdn);
	}

	// //calculate price on item
	// if(doc.quantity && doc.price){
	    
	//     frappe.model.set_value(doc.doctype, doc.name, 'total', Number.parseFloat(doc.price) * Number.parseFloat(doc.quantity));
	// }

	// //calculate invoice total
	// frm.set_value('total_amount', calculate_invoice_total(frm.doc.items));
    },
    quantity(frm, cdt, cdn){
	var doc = locals[cdt][cdn];

	if(doc.item && doc.quantity && doc.price){
	    calculate_item_total(frm, cdt, cdn);
	}

	// //calculate price on item
	// if(doc.quantity && doc.price){
	//     frappe.model.set_value(doc.doctype, doc.name, 'total', Number.parseFloat(doc.price) * Number.parseFloat(doc.quantity));
	// }

	// //calculate invoice total
	// frm.set_value('total_amount', calculate_invoice_total(frm.doc.items));
    },
    price(frm, cdt, cdn){
	var doc = locals[cdt][cdn];

	if(doc.item && doc.quantity && doc.price){
	    calculate_item_total(frm, cdt, cdn);
	}

	// //calculate price on item
	// if(doc.quantity && doc.price){
	//     frappe.model.set_value(doc.doctype, doc.name, 'total', Number.parseFloat(doc.price) * Number.parseFloat(doc.quantity));
	// }

	// //calculate invoice total
	// frm.set_value('total_amount', calculate_invoice_total(frm.doc.items));
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
