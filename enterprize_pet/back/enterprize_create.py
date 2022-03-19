import os 
import sqlite3

os.remove('enterprize.db')
con = sqlite3.connect('enterprize.db')
cur = con.cursor()

sql_cmd = 'CREATE TABLE IF NOT EXISTS partners ( \
    id integer PRIMARY KEY,  \
    name text NOT NULL,  \
    CONSTRAINT unique_name UNIQUE (name)  \
    ); '
cur.execute(sql_cmd)

sql_cmd = 'CREATE TABLE IF NOT EXISTS tiers ( \
    id integer PRIMARY KEY,  \
    value integer NOT NULL,  \
    short_desc text NOT NULL,  \
    CONSTRAINT unique_value UNIQUE (value),  \
    CONSTRAINT unique_short_desc UNIQUE (short_desc)  \
    ); '
cur.execute(sql_cmd)

sql_cmd = 'CREATE TABLE IF NOT EXISTS offices ( \
    id integer PRIMARY KEY,  \
    name text NOT NULL,  \
    address text NOT NULL,  \
    tier_id integer NOT NULL,  \
    FOREIGN KEY (tier_id) REFERENCES tiers (id),  \
    CONSTRAINT unique_name UNIQUE (name)  \
    ); '
cur.execute(sql_cmd)

sql_cmd = 'CREATE TABLE IF NOT EXISTS projects ( \
    id integer PRIMARY KEY,  \
    name text NOT NULL,  \
    demanded_tier_id integer NOT NULL,  \
    FOREIGN KEY (demanded_tier_id) REFERENCES tiers (id),  \
    CONSTRAINT unique_name UNIQUE (name)  \
    ); '
cur.execute(sql_cmd)

sql_cmd = 'CREATE TABLE IF NOT EXISTS employees ( \
    id integer PRIMARY KEY,  \
    name text NOT NULL,  \
    job_title text NOT NULL,  \
    base_salary integer NOT NULL,  \
    work_email text NOT NULL,  \
    work_state text NOT NULL,  \
    office_id integer NOT NULL,  \
    project_id integer NOT NULL,  \
    FOREIGN KEY (office_id) REFERENCES offices (id),  \
    FOREIGN KEY (project_id) REFERENCES projects (id),  \
    CONSTRAINT unique_work_email UNIQUE (work_email)  \
    ); '
cur.execute(sql_cmd)

sql_cmd = 'CREATE TABLE IF NOT EXISTS deals ( \
    id integer PRIMARY KEY,  \
    short_desc text NOT NULL,  \
    execute_date date NOT NULL,  \
    value integer NOT NULL,  \
    prod_project_id integer NOT NULL,  \
    deal_manager_id integer NOT NULL,  \
    partner_id integer NOT NULL,  \
    FOREIGN KEY (prod_project_id) REFERENCES projects (id),  \
    FOREIGN KEY (deal_manager_id) REFERENCES employees (id),  \
    FOREIGN KEY (partner_id) REFERENCES partners (id),  \
    CONSTRAINT unique_short_desc UNIQUE (short_desc)  \
    ); '
cur.execute(sql_cmd)

sql_cmd = 'CREATE TABLE IF NOT EXISTS revenue ( \
    id integer PRIMARY KEY,  \
    short_desc text NOT NULL,  \
    execute_date date NOT NULL,  \
    value integer NOT NULL,  \
    deal_id integer,  \
    FOREIGN KEY (deal_id) REFERENCES deals (id),  \
    CONSTRAINT unique_short_desc UNIQUE (short_desc)  \
    );'
cur.execute(sql_cmd)

sql_cmd = 'CREATE TABLE IF NOT EXISTS salary_pay ( \
    id integer PRIMARY KEY,  \
    execute_date date NOT NULL,  \
    value integer NOT NULL,  \
    employee_id integer NOT NULL,  \
    FOREIGN KEY (employee_id) REFERENCES employees (id)  \
    ); '
cur.execute(sql_cmd)

sql_cmd = 'CREATE TABLE IF NOT EXISTS capital ( \
    id integer PRIMARY KEY,  \
    short_desc text NOT NULL,  \
    execute_date date NOT NULL,  \
    value integer NOT NULL,  \
    project_spend_id integer,  \
    office_spend_id integer,  \
    FOREIGN KEY (project_spend_id) REFERENCES projects (id),  \
    FOREIGN KEY (office_spend_id) REFERENCES offices (id),  \
    CONSTRAINT unique_short_desc UNIQUE (short_desc)  \
    ); '
cur.execute(sql_cmd)

con.commit()