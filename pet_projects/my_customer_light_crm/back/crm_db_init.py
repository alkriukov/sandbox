import os
import sqlite3

db_filename = 'crm.db'
if os.path.exists(db_filename):
    os.remove(db_filename)

crm_db_con = sqlite3.connect(db_filename)
crm_db_cur = crm_db_con.cursor()

sql_cmd = []
sql_cmd.append('CREATE TABLE IF NOT EXISTS service_types ( \
    id integer PRIMARY KEY,  \
    title text NOT NULL,  \
    tech_codes text NOT NULL,  \
    CONSTRAINT unique_title UNIQUE (title)  \
    ); ')
sql_cmd.append('CREATE TABLE IF NOT EXISTS base_service_types ( \
    id integer PRIMARY KEY,  \
    title text NOT NULL,  \
    service_type_id integer NOT NULL,  \
    FOREIGN KEY (service_type_id) REFERENCES service_types (id),  \
    CONSTRAINT unique_title UNIQUE (title)  \
    ); ')
sql_cmd.append('CREATE TABLE IF NOT EXISTS services_usage_types ( \
    id integer PRIMARY KEY,  \
    title text NOT NULL,  \
    CONSTRAINT unique_title UNIQUE (title)  \
    ); ')
sql_cmd.append('CREATE TABLE IF NOT EXISTS service_usage_costs ( \
    id integer PRIMARY KEY,  \
    title text NOT NULL,  \
    default_pay integer NOT NULL,  \
    pay_period text NOT NULL,  \
    base_service_type_id integer,  \
    service_type_id integer NOT NULL,  \
    services_usage_type_id integer NOT NULL,  \
    FOREIGN KEY (base_service_type_id) REFERENCES base_service_types (id),  \
    FOREIGN KEY (service_type_id) REFERENCES service_types (id),  \
    FOREIGN KEY (services_usage_type_id) REFERENCES services_usage_types (id),  \
    CONSTRAINT unique_title UNIQUE (title)  \
    ); ')

sql_cmd.append('CREATE TABLE IF NOT EXISTS customers ( \
    id integer PRIMARY KEY,  \
    name text NOT NULL,  \
    address text NOT NULL,  \
    phone_number integer NOT NULL,  \
    balance integer NOT NULL,  \
    base_service_type_id integer NOT NULL,  \
    FOREIGN KEY (base_service_type_id) REFERENCES base_service_types (id),  \
    CONSTRAINT unique_phone_number UNIQUE (phone_number)  \
    ); ')
sql_cmd.append('CREATE TABLE IF NOT EXISTS active_services ( \
    id integer PRIMARY KEY,  \
    customer_id integer NOT NULL,  \
    service_type_id integer NOT NULL,  \
    FOREIGN KEY (customer_id) REFERENCES customers (id),  \
    FOREIGN KEY (service_type_id) REFERENCES service_types (id)  \
    ); ')
sql_cmd.append('CREATE TABLE IF NOT EXISTS customer_cards ( \
    id integer PRIMARY KEY,  \
    title text NOT NULL,  \
    description text NOT NULL,  \
    customer_id integer NOT NULL,  \
    FOREIGN KEY (customer_id) REFERENCES customers (id)  \
    ); ')
sql_cmd.append('CREATE TABLE IF NOT EXISTS customer_services_usages ( \
    id integer PRIMARY KEY,  \
    title text NOT NULL,  \
    details_info text NOT NULL,  \
    usage_datetime datetime NOT NULL,  \
    usage_amount integer NOT NULL,  \
    charged_value integer NOT NULL,  \
    customer_id integer NOT NULL,  \
    service_usage_cost_id integer NOT NULL,  \
    FOREIGN KEY (customer_id) REFERENCES customers (id),   \
    FOREIGN KEY (service_usage_cost_id) REFERENCES service_usage_costs (id)  \
    ); ')

for command in sql_cmd:
    print(command)
    crm_db_cur.execute(command)

crm_db_con.commit()
