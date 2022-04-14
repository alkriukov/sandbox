import crm_db_op_svc

def add_service_type(db_filename, title, tech_codes):
    table = 'service_types'
    direct_data = { 'title':      title,
                    'tech_codes': tech_codes, }
    data_for_ids = { }
    add_new_item_to_table(db_filename, table, direct_data, data_for_ids)

def add_base_service_type(db_filename, title, service_type_title):
    table = 'base_service_types'
    direct_data = { 'title': title, }
    data_for_ids = { 'service_type_id': ('service_types', 'title', service_type_title), }
    add_new_item_to_table(db_filename, table, direct_data, data_for_ids)

def add_services_usage_type(db_filename, title):
    table = 'services_usage_types'
    direct_data = { 'title': title, }
    data_for_ids = { }
    add_new_item_to_table(db_filename, table, direct_data, data_for_ids)

def add_service_usage_cost(db_filename, title, default_pay, pay_period, service_type_title, services_usage_type_title, base_service_type_title=''):
    table = 'service_usage_costs'
    direct_data = { 'title':       title,
                    'default_pay': default_pay,
                    'pay_period':  pay_period, }
    data_for_ids = { 'service_type_id':        ('service_types',        'title', service_type_title),
                     'services_usage_type_id': ('services_usage_types', 'title', services_usage_type_title), 
                     'base_service_type_id':   ('base_service_types',   'title', base_service_type_title), }
    add_new_item_to_table(db_filename, table, direct_data, data_for_ids)

def add_customer(db_filename, name, address, phone_number, balance, base_service_type_title):
    table = 'customers'
    direct_data = { 'name':         name,
                    'address':      address,
                    'phone_number': phone_number,
                    'balance':      balance, }
    data_for_ids = { 'base_service_type_id': ('base_service_types', 'title', base_service_type_title), }
    add_new_item_to_table(db_filename, table, direct_data, data_for_ids)

def add_active_service(db_filename, customer_phone_number, service_type_title):
    table = 'active_services'
    direct_data = { }
    data_for_ids = { 'customer_id':     ('customers',     'phone_number', customer_phone_number),
                     'service_type_id': ('service_types', 'title', service_type_title), }
    add_new_item_to_table(db_filename, table, direct_data, data_for_ids)

def add_customer_card(db_filename, title, description, customer_phone_number):
    table = 'customer_cards'
    direct_data = { 'title':       title,
                    'description': description, }
    data_for_ids = { 'customer_id': ('customers', 'phone_number', customer_phone_number), }
    add_new_item_to_table(db_filename, table, direct_data, data_for_ids)

def add_customer_services_use(db_filename, title, details_info, usage_datetime, usage_amount, charged_value, customer_phone_number, service_usage_cost_title):
    table = 'customer_cards'
    direct_data = { 'title':          title,
                    'details_info':   details_info,
                    'usage_datetime': usage_datetime,
                    'usage_amount':   usage_amount,
                    'charged_value':  charged_value, }
    data_for_ids = { 'customer_id':           ('customers',           'phone_number', customer_phone_number),
                     'service_usage_cost_id': ('service_usage_costs', 'title', service_usage_cost_title), }
    add_new_item_to_table(db_filename, table, direct_data, data_for_ids)
