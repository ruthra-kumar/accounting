frappe.provide("frappe.treeview_settings")

frappe.treeview_settings["Accounts"] = {
    title: __("Chart of Accounts"),
    on_get_node: function(nodes, deep=false){
	console.log(nodes);

	if(deep){
	    accounts = nodes.reduce((acc, node) => [...acc, ...node.data],[])
	}
	else{
	    accounts = nodes;
	}
	req = { 'deep':deep, 'nodes': nodes };
	frappe.call('accounting.accounting.doctype.accounts.utils.get_node_balances',{
	    'nodes': accounts
	})
	    .then(r => {
		if(r || r.message){
		    for(let account of r.message){
			node = cur_tree.nodes[account.name];
			node.data.balance = account.balance;
			$('<span class="balance-area pull-right">'
			  + new Intl.NumberFormat('en-IN',{style: 'currency', currency:'INR'}).format(node.data.balance)
			  + " "
			  + ((node.data.balance > 0) ? 'Dr': 'Cr')
			 + '</span>').insertBefore(node.$ul);
		    }
		}
	    })
    }
}
