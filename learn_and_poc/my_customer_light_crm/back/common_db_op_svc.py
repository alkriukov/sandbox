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

def db_operation(db_filename, sql_cmd, logging_level=2):
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

def get_id_by_field(db_filename, table, field, value):
    run_sql = check_parameters({'table': table, 'field': field, 'value': value})
    if not str(value).lstrip('-').isdigit():
        value = '"' + value + '"'
    sql_cmd = 'SELECT id FROM ' + table + ' WHERE ' + field + '=' + value + ';'
    if run_sql:
        id = db_operation(db_filename, sql_cmd)
    return id

def delete_item(db_filename, table, field, value):
    run_sql = check_parameters({'table': table, 'field': field, 'value': value})
    if not str(value).lstrip('-').isdigit():
        value = '"' + value + '"'
    sql_cmd = 'DELETE FROM ' + table + ' WHERE ' + field + '=' + value + ';'
    if run_sql:
        db_operation(db_filename, sql_cmd)

def modify_item(db_filename, table, search_column, search_value, new_data_dict):
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
        db_operation(db_filename, sql_cmd)

def add_data_to_table(db_filename, table_name, data):
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
        db_operation(db_filename, sql_cmd)

def add_new_item_to_table(db_filename, table, direct_data, data_for_ids):
    new_item_data = dict(direct_data)
    add_data = False
    try:
        for insert_field in data_for_ids.keys():
            (table_name, field_name, search_value) = data_for_ids[insert_field]
            ids = get_id_by_field(db_filename, table_name, field_name, search_value)
            if len(ids) == 1:
                new_item_data[insert_field] = str(ids[0][0])
        add_data = True
    except (IndexError, TypeError) as e:
        print('CANT GET SINGLE ID: ' + str(data_for_ids[insert_field]) + '\n' + str(ids))
        print(e)
    if add_data:
        add_data_to_table(db_filename, table, new_item_data)
