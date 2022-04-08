import os
import shutil
import sqlite3

db_filename = 'crm_phone_calls.db'
if os.path.exists(db_filename):
    os.remove(db_filename)
raw_db_filename = 'crm.db'
shutil.copyfile(raw_db_filename, db_filename)

crm_db_con = sqlite3.connect(db_filename)
crm_db_cur = crm_db_con.cursor()

sql_cmd = []
sql_cmd.append('INSERT INTO service_types  \
    (title, tech_codes)  \
    VALUES  \
    ("messaging", "messaging_out_of_package"),  \
    ("calls", "calls_out_of_package"),  \
    ("up_balance", "up_balance"),  \
    ("tariff_1", "tariff_1"),  \
    ("tariff_2", "tariff_2"),  \
    ("500_min_calls", "calls_package_500_min");')
sql_cmd.append('INSERT INTO base_service_types  \
    (title, service_type_id)  \
    VALUES  \
    ("tariff_1", (SELECT id FROM service_types WHERE title="tariff_1")),  \
    ("tariff_2", (SELECT id FROM service_types WHERE title="tariff_2"));')
sql_cmd.append('INSERT INTO services_usage_types  \
    (title)  \
    VALUES  \
    ("add"),  \
    ("remove"),  \
    ("use");')
sql_cmd.append('INSERT INTO service_usage_costs  \
    (title, default_pay, pay_period, service_type_id, services_usage_type_id, base_service_type_id)  \
    VALUES  \
    ("msg_add",           0, "0",       (SELECT id FROM service_types WHERE title="messaging"), (SELECT id from services_usage_types WHERE title="add"),    NULL),  \
    ("msg_remove",        0, "0",       (SELECT id FROM service_types WHERE title="messaging"), (SELECT id from services_usage_types WHERE title="remove"), NULL),  \
    ("msg_use_tariff_1",  2, "0",       (SELECT id FROM service_types WHERE title="messaging"), (SELECT id from services_usage_types WHERE title="use"),    (SELECT id FROM base_service_types WHERE title="tariff_1")),  \
    ("msg_use_tariff_2",  1, "0",       (SELECT id FROM service_types WHERE title="messaging"), (SELECT id from services_usage_types WHERE title="use"),    (SELECT id FROM base_service_types WHERE title="tariff_2")),  \
    ("call_add",          0, "0",       (SELECT id FROM service_types WHERE title="calls"), (SELECT id from services_usage_types WHERE title="add"),    NULL),  \
    ("call_remove",       0, "0",       (SELECT id FROM service_types WHERE title="calls"), (SELECT id from services_usage_types WHERE title="remove"), NULL),  \
    ("call_on_tariff_1",  2, "0",       (SELECT id FROM service_types WHERE title="calls"), (SELECT id from services_usage_types WHERE title="use"),    (SELECT id FROM base_service_types WHERE title="tariff_1")),  \
    ("call_on_tariff_2",  1, "0",       (SELECT id FROM service_types WHERE title="calls"), (SELECT id from services_usage_types WHERE title="use"),    (SELECT id FROM base_service_types WHERE title="tariff_2")),  \
    ("up_balance_use",   -1, "0",       (SELECT id FROM service_types WHERE title="up_balance"), (SELECT id from services_usage_types WHERE title="use"),    NULL),  \
    ("up_balance_add",    0, "0",       (SELECT id FROM service_types WHERE title="up_balance"), (SELECT id from services_usage_types WHERE title="add"),     NULL),  \
    ("up_balance_remove", 0, "0",       (SELECT id FROM service_types WHERE title="up_balance"), (SELECT id from services_usage_types WHERE title="remove"), NULL),  \
    ("Tariff_1_pay",      0, "1",       (SELECT id FROM service_types WHERE title="tariff_1"), (SELECT id from services_usage_types WHERE title="use"),     (SELECT id FROM base_service_types WHERE title="tariff_1")),  \
    ("Tariff_1_add",    100, "0",       (SELECT id FROM service_types WHERE title="tariff_1"), (SELECT id from services_usage_types WHERE title="add"),     NULL),  \
    ("Tariff_1_remove",   0, "0",       (SELECT id FROM service_types WHERE title="tariff_1"), (SELECT id from services_usage_types WHERE title="remove"),  (SELECT id FROM base_service_types WHERE title="tariff_1")),  \
    ("Tariff_2_pay",    300, "month_1", (SELECT id FROM service_types WHERE title="tariff_2"), (SELECT id from services_usage_types WHERE title="use"),    (SELECT id FROM base_service_types WHERE title="tariff_2")),  \
    ("Tariff_2_add",      0, "0",       (SELECT id FROM service_types WHERE title="tariff_2"), (SELECT id from services_usage_types WHERE title="add"),     NULL),  \
    ("Tariff_2_remove",   0, "0",       (SELECT id FROM service_types WHERE title="tariff_2"), (SELECT id from services_usage_types WHERE title="remove"), (SELECT id FROM base_service_types WHERE title="tariff_2")),  \
    ("500_in_org_pay",  100, "month_1", (SELECT id FROM service_types WHERE title="500_min_calls"), (SELECT id from services_usage_types WHERE title="use"),    (SELECT id FROM base_service_types WHERE title="tariff_2")),  \
    ("500_in_org_add",    0, "0",       (SELECT id FROM service_types WHERE title="500_min_calls"), (SELECT id from services_usage_types WHERE title="add"),     (SELECT id FROM base_service_types WHERE title="tariff_2")),  \
    ("500_in_org_remove", 0, "0",       (SELECT id FROM service_types WHERE title="500_min_calls"), (SELECT id from services_usage_types WHERE title="remove"), NULL);')

sql_cmd.append('INSERT INTO customers  \
    (name, address, phone_number, balance, base_service_type_id)  \
    VALUES  \
    ("Alyona A", "Moscow, K st 122, 25",  9991748345, 100, (SELECT id FROM base_service_types WHERE title="tariff_1")),  \
    ("Viktor V", "Kursk, L ave 88, 113",  9998375223, 100, (SELECT id FROM base_service_types WHERE title="tariff_2")),  \
    ("Denis D",  "Novgorod, V per 8, 11", 9995492334, 100, (SELECT id FROM base_service_types WHERE title="tariff_2"));')
sql_cmd.append('INSERT INTO active_services  \
    (customer_id, service_type_id)  \
    VALUES  \
    ((SELECT id FROM customers WHERE phone_number=9991748345), (SELECT id FROM service_types WHERE title="messaging")),  \
    ((SELECT id FROM customers WHERE phone_number=9991748345), (SELECT id FROM service_types WHERE title="calls")),  \
    ((SELECT id FROM customers WHERE phone_number=9991748345), (SELECT id FROM service_types WHERE title="up_balance")),  \
    ((SELECT id FROM customers WHERE phone_number=9991748345), (SELECT id FROM service_types WHERE title="tariff_1")),  \
    ((SELECT id FROM customers WHERE phone_number=9998375223), (SELECT id FROM service_types WHERE title="messaging")),  \
    ((SELECT id FROM customers WHERE phone_number=9998375223), (SELECT id FROM service_types WHERE title="calls")),  \
    ((SELECT id FROM customers WHERE phone_number=9998375223), (SELECT id FROM service_types WHERE title="up_balance")),  \
    ((SELECT id FROM customers WHERE phone_number=9998375223), (SELECT id FROM service_types WHERE title="tariff_2")),  \
    ((SELECT id FROM customers WHERE phone_number=9995492334), (SELECT id FROM service_types WHERE title="messaging")),  \
    ((SELECT id FROM customers WHERE phone_number=9995492334), (SELECT id FROM service_types WHERE title="calls")),  \
    ((SELECT id FROM customers WHERE phone_number=9995492334), (SELECT id FROM service_types WHERE title="up_balance")),  \
    ((SELECT id FROM customers WHERE phone_number=9995492334), (SELECT id FROM service_types WHERE title="tariff_2")),  \
    ((SELECT id FROM customers WHERE phone_number=9995492334), (SELECT id FROM service_types WHERE title="500_min_calls"));')
sql_cmd.append('INSERT INTO customer_cards  \
    (title, description, customer_id)  \
    VALUES  \
    ("Personal manager support", "Forward all support requests from customer to Personal Manager. Support id 12", (SELECT id FROM customers WHERE phone_number=9995492334));')

for command in sql_cmd:
    print(command)
    crm_db_cur.execute(command)

crm_db_con.commit()
