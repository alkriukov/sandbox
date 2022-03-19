import os 
import sqlite3

def check_parameters(names):
    check_result = False
    symbols_not_allowed = ["'", ";"]
    for sym in symbols_not_allowed:
        for key in names.keys():
            if sym in key or sym in str(names[key]):
                break
    else:
        check_result = True
    return check_result

def db_operation(sql_cmd, logging_level=2):
    db_filename = 'enterprize.db'
    rows = ''
    if logging_level >= 2:
        print(sql_cmd)
    try:
        con = sqlite3.connect(db_filename)
        cur = con.cursor()
        cur.execute(sql_cmd)
        rows = cur.fetchall()
        con.commit()
        con.close()
    except sqlite3.IntegrityError as e:
        print(e)
    return rows

def get_id_by_field(table, field, value):
    run_sql = check_parameters({'table': table, 'field': field, 'value': value})
    if not str(value).lstrip('-').isdigit():
        value = '"' + value + '"'
    sql_cmd = 'SELECT id FROM ' + table + ' WHERE ' + field + '=' + value + ';'
    if run_sql:
        id = db_operation(sql_cmd)
    return id

def delete_item(table, field, value):
    run_sql = check_parameters({'table': table, 'field': field, 'value': value})
    if not str(value).lstrip('-').isdigit():
        value = '"' + value + '"'
    sql_cmd = 'DELETE FROM ' + table + ' WHERE ' + field + '=' + value + ';'
    if run_sql:
        db_operation(sql_cmd)

def modify_item(table, search_column, search_value, new_data_dict):
    data = { 'table': table, 'search_column': search_column, 'search_value': search_value }
    run_sql = check_parameters(data) and check_parameters(new_data_dict)
    if not str(search_value).lstrip('-').isdigit():
        search_value = '"' + search_value + '"'
    sql_assign_values = []
    for k in new_data_dict.keys():
        if not new_data_dict[k]:
            sql_assign_values.append(k + '=NULL')
        elif str(new_data_dict[k]).lstrip('-').isdigit():
            sql_assign_values.append(k + '=' + new_data_dict[k])
        else:
            sql_assign_values.append(k + '="' + new_data_dict[k] + '"')
    sql_cmd = 'UPDATE ' + data['table'] + \
             ' SET ' + ', '.join(sql_assign_values) + \
             ' WHERE ' + search_column + '=' + search_value + ';'
    if run_sql:
        db_operation(sql_cmd)

def add_data_to_table(table_name, data):
    run_sql = check_parameters({'table': table_name}) and check_parameters(data)
    data_keys = list(data.keys())
    sql_data = []
    for key in data_keys:
        if not data[key]:
            sql_data.append('NULL')
        elif str(data[key]).lstrip('-').isdigit():
            sql_data.append(data[key])
        else:
            sql_data.append('"' + data[key] + '"')
    sql_prefix = 'INSERT INTO ' + table_name + ' (' + ', '.join(data_keys) + ') VALUES ('
    sql_cmd = sql_prefix + ', '.join(sql_data) + ');'
    if run_sql:
        db_operation(sql_cmd)

def add_new_item_to_table(table, direct_data, data_for_ids):
    new_item_data = dict(direct_data)
    add_data = False
    try:
        for insert_field in data_for_ids.keys():
            (table_name, field_name, search_value) = data_for_ids[insert_field]
            ids = get_id_by_field(table_name, field_name, search_value)
            if len(ids) == 1:
                new_item_data[insert_field] = str(ids[0][0])
        add_data = True
    except (IndexError, TypeError) as e:
        print('CANT GET SINGLE ID: ' + str(data_for_ids[insert_field]) + '\n' + str(ids))
        print(e)
    if add_data:
        add_data_to_table(table, new_item_data)

def add_partner(name):
    table = 'partners'
    direct_data = { 'name': name, }
    data_for_ids = { }
    add_new_item_to_table(table, direct_data, data_for_ids)

def add_tier(value, short_desc):
    table = 'tiers'
    direct_data = { 'value':      value,
                    'short_desc': short_desc, }
    data_for_ids = { }
    add_new_item_to_table(table, direct_data, data_for_ids)

def add_office(name, address, tier):
    table = 'offices'
    direct_data = { 'name':    name,
                    'address': address, }
    data_for_ids = { 'tier_id':  ('tiers', 'value', tier), }
    add_new_item_to_table(table, direct_data, data_for_ids)

def add_project(name, demanded_tier):
    table = 'projects'
    direct_data = { 'name': name, }
    data_for_ids = { 'demanded_tier_id':  ('tiers', 'value', demanded_tier), }
    add_new_item_to_table(table, direct_data, data_for_ids)

def add_employee(name, job_title, base_salary, work_email, work_state, office_name, project_name):
    table = 'employees'
    direct_data = { 'name':        name,
                    'job_title':   job_title,
                    'base_salary': base_salary,
                    'work_email':  work_email,
                    'work_state':  work_state, }
    data_for_ids = { 'office_id':  ('offices', 'name', office_name),
                     'project_id': ('projects', 'name', project_name), }
    add_new_item_to_table(table, direct_data, data_for_ids)

def add_deal(short_desc, execute_date, value, prod_project, manager_email, partner):
    table = 'deals'
    direct_data = { 'short_desc':   short_desc,
                    'execute_date': execute_date,
                    'value': value, }
    data_for_ids = { 'prod_project_id': ('projects', 'name', prod_project),
                     'deal_manager_id': ('employees', 'work_email', manager_email),
                     'partner_id':      ('partners', 'name', partner), }
    add_new_item_to_table(table, direct_data, data_for_ids)

def add_revenue(revenue_short_desc, execute_date, value, deal_short_desc):
    table = 'revenue'
    direct_data = { 'short_desc':   revenue_short_desc,
                    'execute_date': execute_date,
                    'value': value, }
    data_for_ids = { 'deal_id': ('deals', 'short_desc', deal_short_desc), }
    add_new_item_to_table(table, direct_data, data_for_ids)

def add_salary_pay(execute_date, value, employee_work_email):
    table = 'salary_pay'
    direct_data = { 'execute_date': execute_date,
                    'value':        value, }
    data_for_ids = { 'employee_id': ('employees', 'work_email', employee_work_email), }
    add_new_item_to_table(table, direct_data, data_for_ids)

def add_capital_spending(short_desc, execute_date, value, project_name = '', office_name = ''):
    table = 'capital'
    direct_data = { 'short_desc':   short_desc,
                    'execute_date': execute_date,
                    'value':        value, }
    data_for_ids = { 'project_spend_id': ('projects', 'name', project_name),
                     'office_spend_id':  ('offices', 'name', office_name), }
    add_new_item_to_table(table, direct_data, data_for_ids)
