// Copyright (c) 2016, ruthra and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["GL Report"] = {
    "filters": [
	{
		"fieldname":"account",
		"label": __("Account"),
		"fieldtype": "Data",
		// "default": frappe.defaults.get_user_default("company")
	},
	{
		"fieldname":"type",
		"label": __("Type"),
		"fieldtype": "Data",
		// "default": frappe.defaults.get_user_default("company")
	},
	{
		"fieldname":"debit",
		"label": __("Debit"),
		"fieldtype": "Currency",
		// "default": frappe.defaults.get_user_default("company")
	},
	{
		"fieldname":"credit",
		"label": __("Credit"),
		"fieldtype": "Currency",
		// "default": frappe.defaults.get_user_default("company")
	},
	{
		"fieldname":"balance",
		"label": __("Balance"),
		"fieldtype": "Currency",
		// "default": frappe.defaults.get_user_default("company")
	}

    ]
};
