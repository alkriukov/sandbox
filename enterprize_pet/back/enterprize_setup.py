import os 
import sqlite3

con = sqlite3.connect('enterprize.db')
cur = con.cursor()

sql_cmd = 'INSERT INTO tiers (value, short_desc)  \
    VALUES  \
    (1, "basic"),  \
    (2, "dedicated"),  \
    (3, "advanced"); '
cur.execute(sql_cmd)

sql_cmd = 'INSERT INTO offices (name, address, tier_id)  \
    VALUES  \
    ("MS1", "Moscow, V st. 193", (SELECT id from tiers WHERE value=3)),  \
    ("MS2", "Moscow, M per. 26", (SELECT id from tiers WHERE value=1)),  \
    ("NN1",  "N.Novgorod, K st. 4", (SELECT id from tiers WHERE value=2));'
cur.execute(sql_cmd)

sql_cmd = 'INSERT INTO projects (name, demanded_tier_id)  \
    VALUES  \
    ("operations", (SELECT id from tiers WHERE value=3)),  \
    ("sales", (SELECT id from tiers WHERE value=1)),  \
    ("client_dev", (SELECT id from tiers WHERE value=2)),  \
    ("server_dev", (SELECT id from tiers WHERE value=2));'
cur.execute(sql_cmd)

sql_cmd = 'INSERT INTO employees (name, job_title, base_salary, work_email, work_state, office_id, project_id)  \
    VALUES  \
    ("A Aaa", "client products director", 400000, "a.aaa@my.ru", "working", (SELECT id FROM offices WHERE name="MS1"), (SELECT id FROM projects WHERE name="client_dev")),  \
    ("B Bbb", "sr developer", 300000, "b.bbb@my.ru", "working", (SELECT id FROM offices WHERE name="MS1"), (SELECT id FROM projects WHERE name="client_dev")),  \
    ("C Ccc", "sr developer", 300000, "c.ccc@my.ru", "working", (SELECT id FROM offices WHERE name="MS1"), (SELECT id FROM projects WHERE name="client_dev")),  \
    ("D Ddd", "developer", 200000, "d.ddd@my.ru", "working", (SELECT id FROM offices WHERE name="MS1"), (SELECT id FROM projects WHERE name="client_dev")),  \
    ("E Eee", "developer", 200000, "e.eee@my.ru", "working", (SELECT id FROM offices WHERE name="MS1"), (SELECT id FROM projects WHERE name="client_dev")),  \
    ("F Fff", "client products assembly", 200000, "f.fff@my.ru", "working", (SELECT id FROM offices WHERE name="MS1"), (SELECT id FROM projects WHERE name="client_dev")),  \
    ("G Ggg", "client products assembly", 200000, "g.ggg@my.ru", "working", (SELECT id FROM offices WHERE name="MS1"), (SELECT id FROM projects WHERE name="client_dev")),  \
    ("H Hhh", "server products director", 400000, "h.hhh@my.ru", "working", (SELECT id FROM offices WHERE name="NN1"), (SELECT id FROM projects WHERE name="server_dev")),  \
    ("I Iii", "sr developer", 300000, "i.iii@my.ru", "working", (SELECT id FROM offices WHERE name="NN1"), (SELECT id FROM projects WHERE name="server_dev")),  \
    ("J Jjj", "sr developer", 300000, "j.jjj@my.ru", "working", (SELECT id FROM offices WHERE name="NN1"), (SELECT id FROM projects WHERE name="server_dev")),  \
    ("K Kkk", "developer", 200000, "k.kkk@my.ru", "working", (SELECT id FROM offices WHERE name="NN1"), (SELECT id FROM projects WHERE name="server_dev")),  \
    ("L Lll", "server products assembly", 200000, "l.lll@my.ru", "working", (SELECT id FROM offices WHERE name="NN1"), (SELECT id FROM projects WHERE name="server_dev")),  \
    ("M Mmm", "sales manager", 250000, "m.mmm@my.ru", "working", (SELECT id FROM offices WHERE name="NN1"), (SELECT id FROM projects WHERE name="sales")),  \
    ("N Nnn", "sr sales", 150000, "n.nnn@my.ru", "working", (SELECT id FROM offices WHERE name="MS2"), (SELECT id FROM projects WHERE name="sales")),  \
    ("O Ooo", "sales", 100000, "o.ooo@my.ru", "working", (SELECT id FROM offices WHERE name="MS2"), (SELECT id FROM projects WHERE name="sales")),  \
    ("P Ppp", "sr sales", 150000, "p.ppp@my.ru", "working", (SELECT id FROM offices WHERE name="NN1"), (SELECT id FROM projects WHERE name="sales")),  \
    ("Q Qqq", "sales", 100000, "q.qqq@my.ru", "working", (SELECT id FROM offices WHERE name="NN1"), (SELECT id FROM projects WHERE name="sales")),  \
    ("R Rrr", "legal", 600000, "r.rrr@my.ru", "working", (SELECT id FROM offices WHERE name="MS1"), (SELECT id FROM projects WHERE name="operations")),  \
    ("S Sss", "cto", 600000, "s.sss@my.ru", "working", (SELECT id FROM offices WHERE name="MS1"), (SELECT id FROM projects WHERE name="operations")),  \
    ("T Ttt", "hr", 400000, "t.ttt@my.ru", "working", (SELECT id FROM offices WHERE name="MS1"), (SELECT id FROM projects WHERE name="operations")),  \
    ("U Uuu", "cfo", 400000, "u.uuu@my.ru", "working", (SELECT id FROM offices WHERE name="MS1"), (SELECT id FROM projects WHERE name="operations")),  \
    ("V Vvv", "ceo", 800000, "v.vvv@my.ru", "working", (SELECT id FROM offices WHERE name="MS1"), (SELECT id FROM projects WHERE name="operations"));'
cur.execute(sql_cmd)

con.commit()
