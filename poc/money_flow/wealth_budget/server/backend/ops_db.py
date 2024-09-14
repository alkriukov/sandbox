from db_connect import DBconn, DBw



def isUserInDb(nick_v):
    DBw.execute('SELECT 1 FROM nicks WHERE nick = %s', (nick_v,))
    return (DBw.fetchone() != None)

def getUserById(id_v):
    DBw.execute('SELECT * FROM users WHERE id = %s', (id_v,))
    return DBw.fetchone()

def getUserByNick(nick_v):
    DBw.execute('SELECT * FROM users WHERE nick = %s', (nick_v,))
    return DBw.fetchone()

def getUserIdByNick(nick_v):
    user_id = None
    DBw.execute('SELECT id FROM nicks WHERE nick = %s', (nick_v,))
    user_info = DBw.fetchone()
    if isinstance(user_info, dict) and 'id' in user_info.keys() and isinstance(user_info['id'], int):
        user_id = user_info['id']
    return user_id

def getUserIdByDeviceToken(token_v):
    DBw.execute('SELECT user_id FROM devices WHERE token = %s', (token_v,))
    return DBw.fetchone()

def addUser(nick_v, passwd_v, reg_dt_v, sets_v):
    DBw.execute('INSERT INTO users (nick, passwd, registered, settings) VALUES (%s, %s, %s, %s)', (nick_v, passwd_v, reg_dt_v, sets_v))
    DBconn.commit()
    return DBw.lastrowid

def changeUserInfo(id_v, new_sets_v):
    DBw.execute('UPDATE users SET settings = %s WHERE id = %s', (new_sets_v, id_v))
    DBconn.commit()
    return DBw.rowcount

def changeUserData(id_v, new_sets_v, new_passwd_v):
    DBw.execute('UPDATE users SET settings = %s, passwd = %s WHERE id = %s', (new_sets_v, new_passwd_v, id_v))
    DBconn.commit()
    return DBw.rowcount

def delUser(id_v):
    DBw.execute('DELETE FROM users WHERE id = %s', (id_v,))
    DBconn.commit()
    return DBw.rowcount



def getUserDevices(user_id_v):
    DBw.execute('SELECT id, generic_info FROM device_infos WHERE user_id = %s', (user_id_v,))
    return DBw.fetchall()

def deviceBelongsToUser(device_id_v, user_id_v):
    res = False
    DBw.execute('SELECT user_id FROM device_infos WHERE id = %s', (device_id_v,))
    data = DBw.fetchone()
    if isinstance(data, dict) and 'user_id' in data.keys() and data['user_id'] == user_id_v:
        res = True
    return res

def addDevice(token_v, info_v, user_id_v, reg_dt_v):
    DBw.execute('INSERT INTO devices (token, registered, generic_info, user_id) VALUES (%s, %s, %s, %s)', (token_v, reg_dt_v, info_v, user_id_v))
    DBconn.commit()
    return DBw.lastrowid

def updateDeviceInfo(id_v, device_info_v):
    DBw.execute('UPDATE device_infos SET generic_info = %s WHERE id = %s', (device_info_v, id_v))
    DBconn.commit()
    return DBw.rowcount

def delDevice(id_v):
    DBw.execute('DELETE FROM devices WHERE id = %s', (id_v,))
    DBconn.commit()
    return DBw.rowcount

def delDeviceByToken(token_v):
    DBw.execute('DELETE FROM devices WHERE token = %s', (token_v,))
    DBconn.commit()
    return DBw.rowcount



def getProjectById(id_v):
    DBw.execute('SELECT * FROM projects WHERE id = %s', (id_v,))
    return DBw.fetchone()

def addProject(title_v, sets_v, p_status_v):
    DBw.execute('INSERT INTO projects (title, settings, p_status) VALUES (%s, %s, %s)', (title_v, sets_v, p_status_v))
    DBconn.commit()
    return DBw.lastrowid

def updateExistingProject(id_v, title_v, sets_v, p_status_v):
    DBw.execute('UPDATE projects SET title = %s, settings = %s, p_status = %s WHERE id = %s', (title_v, sets_v, p_status_v, id_v))
    DBconn.commit()
    return DBw.rowcount

def delProject(id_v):
    DBw.execute('DELETE FROM projects WHERE id = %s', (id_v,))
    DBconn.commit()
    return DBw.rowcount

def cleanUserlessProjects():
    DBw.execute('DELETE FROM projects WHERE NOT EXISTS (SELECT 1 FROM user_projects WHERE project_id = projects.id)')
    DBconn.commit()
    return DBw.rowcount



def getUserRoleInProject(user_id_v, project_id_v):
    role = None
    DBw.execute('SELECT user_role FROM user_projects WHERE user_id = %s AND project_id = %s', (user_id_v, project_id_v))
    role_data = DBw.fetchone()
    if isinstance(role_data, dict) and 'user_role' in role_data.keys():
        role = role_data["user_role"]
    return role

def getUserProjectsIDs(user_id_v):
    DBw.execute('SELECT project_id FROM user_projects WHERE user_id = %s', (user_id_v,))
    proj_ids = []
    for pr in DBw.fetchall():
        if isinstance(pr, dict) and 'project_id' in pr.keys():
            proj_ids.append(pr['project_id'])
    return proj_ids

def getUserProjects(user_id_v):
    DBw.execute('SELECT id, title, settings, user_role FROM user_project_view WHERE user_id = %s', (user_id_v,))
    return DBw.fetchall()

def addUserToProject(user_id_v, project_id_v, user_role):
    DBw.execute('REPLACE INTO user_projects (user_id, project_id, user_role) VALUES (%s, %s, %s)', (user_id_v, project_id_v, user_role))
    DBconn.commit()
    return DBw.rowcount

def delUserFromProject(user_id_v, project_id_v):
    DBw.execute('DELETE FROM user_projects WHERE user_id = %s AND project_id = %s', (user_id_v, project_id_v))
    DBconn.commit()
    return DBw.rowcount



def getLabel(label_id_v):
    DBw.execute(f'SELECT * FROM labels WHERE id = %s', (label_id_v,))
    return DBw.fetchone()

def getProjectLabels(proj_id_v):
    DBw.execute(f'SELECT * FROM labels WHERE id = %s', (proj_id_v,))
    return DBw.fetchall()

def labelIDInProject(title_v, proj_id_v):
    DBw.execute(f'SELECT 1 FROM labels WHERE title = %s AND project_id = %s', (title_v, proj_id_v))
    label = DBw.fetchone()
    if isinstance(label, dict) and 'id' in label.keys():
        label_id = label['id']
    else:
        label_id = None
    return label_id

def newLabelInProject(title_v, proj_id_v):
    DBw.execute('INSERT INTO labels (title, project_id) VALUES (%s, %s)', (title_v, proj_id_v))
    DBconn.commit()
    return DBw.lastrowid

def updateLabel(label_id_v, new_title_v):
    DBw.execute('UPDATE labels SET title = %s WHERE id = %s', (new_title_v, label_id_v))
    DBconn.commit()
    return DBw.rowcount

def deleteLabel(label_id_v):
    DBw.execute('DELETE FROM labels WHERE id = %s', (label_id_v,))
    DBconn.commit()
    return DBw.rowcount


def getPortfolio(id_v):
    DBw.execute('SELECT * FROM portfolios where id = %s', (id_v,))
    return DBw.fetchone()

def newPortfolio(title_v, props_v, proj_id_v):
    DBw.execute('INSERT INTO portfolios (pf_title, pf_properties, project_id) VALUES (%s, %s, %s)', (title_v, props_v, proj_id_v))
    DBconn.commit()
    return DBw.lastrowid

def editPortfolio(id_v, title_v, props_v):
    DBw.execute('UPDATE portfolios SET pf_title = %s, pf_properties = %s WHERE id = %s', (title_v, props_v, id_v))
    DBconn.commit()
    return DBw.rowcount

def cleanWalletlessPortfolios():
    DBw.execute('DELETE FROM portfolios WHERE NOT EXISTS (SELECT 1 FROM wallets WHERE portfolio_id = portfolios.id)')
    DBconn.commit()
    return DBw.rowcount



def getWallet(id_v):
    DBw.execute('SELECT * FROM wallets_view where id = %s', (id_v,))
    return DBw.fetchone()

def getPortfolioWallets(pf_id_v):
    DBw.execute(f'SELECT * FROM wallets WHERE portfolio_id = %s', (pf_id_v,))
    return DBw.fetchall()

def getProjectWallets(proj_id_v):
    DBw.execute(f'SELECT * FROM wallets_view WHERE project_id = %s', (proj_id_v,))
    return DBw.fetchall()

def newWallet(title_v, props_v, value_v, pf_id_v):
    DBw.execute('INSERT INTO wallets (title, properties, value, portfolio_id) VALUES (%s, %s, %s, %s)', (title_v, props_v, value_v, pf_id_v))
    DBconn.commit()
    return DBw.lastrowid

def editWallet(id_v, title_v, props_v, value_v, pf_id_v):
    DBw.execute('UPDATE wallets SET title = %s, properties = %s, value = %s, portfolio_id = %s WHERE id = %s', (title_v, props_v, value_v, pf_id_v, id_v))
    DBconn.commit()
    return DBw.rowcount

def delWallet(id_v):
    DBw.execute('DELETE FROM wallets WHERE id = %s', (id_v,))
    DBconn.commit()
    return DBw.rowcount



def getTransaction(id_v):
    DBw.execute('SELECT * FROM transactions WHERE id = %s', (id_v,))
    return DBw.fetchone()

def getTransactions(w_id_v):
    DBw.execute('SELECT * FROM transactions WHERE from_wallet_id = %s OR to_wallet_id = %s', (w_id_v, w_id_v))
    return DBw.fetchall()

def newTransaction(date_v, value_v, comment_v, from_w_id_v, to_w_id_v):
    DBw.execute('INSERT INTO transactions (date, value, comment, from_wallet_id, to_wallet_id) VALUES (%s, %s, %s, %s, %s)', (date_v, value_v, comment_v, from_w_id_v, to_w_id_v))
    DBconn.commit()
    return DBw.lastrowid

def editTransaction(date_v, comment_v, id_v):
    DBw.execute('UPDATE transactions SET date = %s, comment = %s WHERE id = %s', (date_v, comment_v, id_v))
    DBconn.commit()
    return DBw.rowcount

def rollbackTransaction(id_v):
    DBw.execute('SELECT value, from_wallet_id, to_wallet_id FROM transactions WHERE id = %s', (id_v,))
    tr_to_rollback = DBw.fetchone()
    ret = 0
    if isinstance(tr_to_rollback, dict) and all(k in tr_to_rollback.keys() for k in ['value', 'from_wallet_id', 'to_wallet_id']):
        tr_value = tr_to_rollback['value']
        from_w_id = tr_to_rollback['from_wallet_id']
        to_w_id = tr_to_rollback['to_wallet_id']
        DBw.execute('UPDATE wallets SET value = value + %s WHERE id = %s)', (tr_value, from_w_id))
        DBw.execute('UPDATE wallets SET value = value - %s WHERE id = %s)', (tr_value, to_w_id))
        DBw.execute('DELETE FROM transactions WHERE id = %s', (id_v,))
        DBconn.commit()
        ret = DBw.rowcount
    return ret

def deleteTransaction(id_v):
    DBw.execute('DELETE FROM transactions WHERE id = %s', (id_v,))
    DBconn.commit()
    return DBw.rowcount
    


def getTransactionsLabelsInProject(proj_id_v):
    DBw.execute(f'SELECT * FROM transaction_label_view WHERE project_id = %s', (proj_id_v,))
    return DBw.fetchall()

def labelTransaction(label_id_v, transaction_id_v):
    DBw.execute('REPLACE INTO transaction_labels (label_id, transaction_id) VALUES (%s, %s)', (label_id_v, transaction_id_v))
    DBconn.commit()
    return DBw.rowcount

def unLabelTransaction(label_id_v, transaction_id_v):
    DBw.execute('DELETE FROM transaction_labels WHERE label_id = %s AND transaction_id = %s', (label_id_v, transaction_id_v))
    DBconn.commit()
    return DBw.rowcount
    



def getSchedule(id_v):
    DBw.execute('SELECT * FROM schedules WHERE id = %s', (id_v,))
    return DBw.fetchone()

def getWalletSchedules(w_id_v):
    DBw.execute('SELECT * FROM schedules WHERE from_wallet_id = %s OR to_wallet_id = %s', (w_id_v, w_id_v))
    return DBw.fetchall()

def getProjectSchedules(proj_id_v):
    wallets = getProjectWallets(proj_id_v)
    w_ids = [w['id'] for w in wallets]
    placeholder = ', '.join([ '%s' * len(w_ids) ])
    DBw.execute(f'SELECT * FROM schedules WHERE from_wallet_id in ({placeholder}) OR to_wallet_id in ({placeholder})', tuple(w_ids) * 2)
    return DBw.fetchall()

def newSchedule(comment_v, date_v, tz_o_m_v, repeat_v, value_v, is_percent_v, from_w_id_v, to_w_id_v):
    DBw.execute('INSERT INTO schedules (comment, next_date, tz_offset_min, repeat_rule, value, value_is_percent, from_wallet_id, to_wallet_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (comment_v, date_v, tz_o_m_v, repeat_v, value_v, is_percent_v, from_w_id_v, to_w_id_v))
    DBconn.commit()
    return DBw.lastrowid

def editSchedule(comment_v, date_v, tz_o_m_v, repeat_v, value_v, is_percent_v, id_v):
    DBw.execute('UPDATE schedules SET comment = %s, next_date = %s, tz_offset_min = %s, repeat_rule = %s, value = %s, value_is_percent = %s WHERE id = %s', (comment_v, date_v, tz_o_m_v, repeat_v, value_v, is_percent_v, id_v))
    DBconn.commit()
    return DBw.rowcount

def deleteSchedule(id_v):
    DBw.execute('DELETE FROM schedules WHERE id = %s', (id_v,))
    DBconn.commit()
    return DBw.rowcount
    


def getSchedulesLabelsInProject(proj_id_v):
    DBw.execute(f'SELECT * FROM schedule_label_view WHERE project_id = %s', (proj_id_v,))
    return DBw.fetchall()

def labelSchedule(label_id_v, schedule_id_v):
    DBw.execute('REPLACE INTO schedule_labels (label_id, schedule_id) VALUES (%s, %s)', (label_id_v, schedule_id_v))
    DBconn.commit()
    return DBw.rowcount

def unLabelSchedule(label_id_v, schedule_id_v):
    DBw.execute('DELETE FROM schedule_labels WHERE label_id = %s AND schedule_id = %s', (label_id_v, schedule_id_v))
    DBconn.commit()
    return DBw.rowcount
    