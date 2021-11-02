// Copyright (c) 2016, ruthra and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["GL Report"] = {
    "filters": [
	{
	    "fieldname":"account",
	    "label": __("Account"),
	    "fieldtype": "Link",
	    "options": "Accounts",
	}

    ],
    "formatter": function(value, row, column, data, default_formatter){
	if(column.fieldtype == 'Currency' && !(value === undefined)){
	    value = new Intl.NumberFormat('en-IN', {style: 'currency', currency:'INR'}).format(value);
	    return "<div style='text-align: right'>"+ value + "</div>";
	}
	return default_formatter(value, row, column, data);
    }
};
