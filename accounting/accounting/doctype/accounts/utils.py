import frappe

def calculate_dr_cr_bal(debit, credit):
    return (debit - credit)

def calculate_leaf_balance(account = None):
    """
    Given a leaf node, calculate the total balance for that account using ledger entries
    'account' - should be a dict obj with 'name' field
    return - total balance on that account
    """

    if account:
        acc_gl_entries = frappe.db.get_list('General Ledger', filters={'account': account['name']}, fields=['debit', 'credit'], order_by='posting_date,posting_time')
        # bal = list(map(lambda x: (x['debit']-x['credit']), acc_gl_entries))
        # # print(reduce(lambda x,y: x+y, bal))
        # print(bal)

        # opening balance
        balance = 0
        for x in acc_gl_entries:
            if account['type'] == 'Nominal':
                balance += (x['credit'] - x['debit'])
            else:
                balance += (x['debit'] - x['credit'])

        return balance

def calculate_group_balance(group):
    """
    Given a group node calculate the total balance by recursive call
    'group' - should be dict obj with 'name' and 'is_group' field
    return - total balance on group node
    """

    child_nodes = frappe.db.get_list('Accounts', filters={'parent_accounts': group.name}, fields=['name', 'type', 'is_group'])

    balance  = 0
    for x in child_nodes:
        if x['is_group']:
            balance += calculate_group_balance(x)
        else:
            balance += calculate_leaf_balance(x)

    return balance


def calculate_balance_on_node(account):
    """
    calculate balance on node.
    'account' - should be a dict obj with name, type and is_group fields
    return 'account' with new field 'balance'.
    """
    if(account['is_group']):
        account['balance'] = calculate_group_balance(account)
    else:
        account['balance'] = calculate_leaf_balance(account)

    return account

def get_all_child_as_list(node):
        """
        Get all child nodes as a list
        node - should be a dict with 'name', 'type' and 'is_group' fields
        return - a list of all child nodes
        """
        if node != None:
                lst = cur_item = []
                stack = []
                stack.append(node)

                while len(stack) != 0:
                        cur_item = stack.pop()
                        lst.append(cur_item)
                        children = frappe.db.get_list('Accounts',filters={'parent_accounts':cur_item['name']}, fields=['name','type','is_group'])
                        for child in children:
                                stack.append(child)

                return lst

@frappe.whitelist()
def get_node_balances(nodes):

    nodes_list = frappe.json.loads(nodes)

    accounts = frappe.db.get_list('Accounts',
                                  filters={'name': ['in', list(map(lambda x: x['value'], nodes_list))]},
                                  fields=['name', 'type', 'is_group'])

    response = list(map(lambda acc: calculate_balance_on_node(acc),accounts))

    return response
