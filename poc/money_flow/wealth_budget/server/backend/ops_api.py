from datetime import datetime

import ops_db as dbOps
import ops_err as errOps
import ops_sec as secOps
import ops_settings as setsOps
import ops_input as inOps



@errOps.handleExceptions
@secOps.authenticateByToken
async def getUserInfo(token = '', nick = None, auth_user_id = None):
    inOps.validateNick(nick)
    user_data = dbOps.getUserById(auth_user_id)
    errOps.validateData(user_data, dict, keys=['nick'])
    if nick != user_data['nick']:
        raise errOps.AuthorizationError()
    return user_data

@errOps.handleExceptions
async def registerNewUser(req = None):
    inp = await inOps.validateRB(req, { 'nick': str, 'passwd': str, 'settings': str, 'device_info': str })
    u_sets = setsOps.userSets(inp["settings"])
    if dbOps.isUserInDb(inp["nick"]):
        resp = { 'error': 'user already exists' }
    else:
        reg_dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_id = dbOps.addUser(inp["nick"], secOps.getPasswd(inp['passwd'], reg_dt), reg_dt, u_sets)
        resp = { 'id': user_id, 'nick': inp["nick"], 'settings': u_sets, }
        raw_token = secOps.newToken(inp["device_info"])
        stored_token = secOps.getToken(raw_token)
        device_id = dbOps.addDevice(stored_token, inp['device_info'], user_id, reg_dt)
        resp.update({ 'device_id': device_id, 'token': raw_token, 'device_info': inp['device_info'] })
    return resp

@errOps.handleExceptions
@secOps.authenticateByToken
async def updateUserInfo(token = '', req = None, auth_user_id = None):
    inp = await inOps.validateRB(req, { 'new_settings': str, 'cur_passwd': str, 'new_passwd': str })
    user_data = dbOps.getUserById(auth_user_id)
    errOps.validateData(user_data, dict, keys=['nick', 'passwd', 'registered'])
    if inp["cur_passwd"] == inp["new_passwd"]:
        n_rows = dbOps.changeUserInfo(auth_user_id, inp["new_settings"])
    else:
        passwd_to_check = secOps.getPasswd(inp['cur_passwd'], user_data['registered'])
        if passwd_to_check != user_data['passwd']:
            raise errOps.AuthenticationError()
        new_passwd = secOps.getPasswd(inp['new_passwd'], user_data['registered'])
        n_rows = dbOps.changeUserData(auth_user_id, inp["new_settings"], new_passwd)
    return { 'updated': n_rows }

@errOps.handleExceptions
@secOps.authenticateByToken
async def deleteUser(token = '', req = None, auth_user_id = None):
    inp = await inOps.validateRB(req, { 'nick': str, 'passwd': str, })
    user_data = dbOps.getUserById(auth_user_id)
    errOps.validateData(user_data, dict, keys=['nick', 'passwd', 'registered'])
    if inp['nick'] != user_data['nick'] or secOps.getPasswd(inp['passwd'], user_data['registered']) != user_data['passwd']:
        raise errOps.AuthenticationError()
    dbOps.delUser(auth_user_id)
    dbOps.cleanUserlessProjects()
    return {'user': 'deleted'}



@errOps.handleExceptions
@secOps.authenticateByToken
async def getDevices(token = '', auth_user_id = None):
    user_devices_info = dbOps.getUserDevices(auth_user_id)
    return { 'devices': user_devices_info }

@errOps.handleExceptions
async def addDeviceWithPassword(req = None):
    inp = await inOps.validateRB(req, { 'nick': str, 'passwd': str, 'device_info': str })
    user_data = dbOps.getUserByNick(inp['nick'])
    errOps.validateData(user_data, dict, keys=['id', 'nick', 'passwd', 'registered'])
    if secOps.getPasswd(inp['passwd'], user_data['registered']) != user_data['passwd']:
        raise errOps.AuthenticationError()
    raw_token = secOps.newToken(inp["device_info"])
    stored_token = secOps.getToken(raw_token)
    device_id = dbOps.addDevice(stored_token, inp['device_info'], user_data['id'], user_data['registered'])
    return { 'device_id': device_id, 'token': raw_token, 'device_info': inp['device_info'] }

@errOps.handleExceptions
@secOps.authenticateByToken
async def updateDeviceInfo(token = '', req = None, device_id = None, auth_user_id = None):
    inOps.validateId(device_id)
    inp = await inOps.validateRB(req, { 'device_info': str })
    if not dbOps.deviceBelongsToUser(device_id, auth_user_id):
        raise errOps.AuthorizationError()
    n_rows = dbOps.updateDeviceInfo(device_id, inp['device_info'])
    return { 'device_id': device_id, 'device_info': inp['device_info'], 'changed': n_rows }

@errOps.handleExceptions
@secOps.authenticateByToken
async def deleteDevice(token = '', device_id = None, auth_user_id = None):
    inOps.validateId(device_id, allow_none = True)
    if device_id == None:
        n_rows = dbOps.delDeviceByToken(secOps.getToken(token))
    else:
        if not dbOps.deviceBelongsToUser(device_id, auth_user_id):
            raise errOps.AuthorizationError()
        n_rows = dbOps.delDevice(device_id)
    return { 'deleted': n_rows }



@errOps.handleExceptions
@secOps.authenticateByToken
async def newProject(token = '', req = None, auth_user_id = None):
    inp = await inOps.validateRB(req, { 'title': str, 'settings': str, 'p_status': str, })
    user_role = 'admin'
    p_sets = setsOps.projSets(inp['settings'])
    proj_id = dbOps.addProject(inp['title'], p_sets, inp['p_status'])
    n_rows = dbOps.addUserToProject(auth_user_id, proj_id, user_role)
    return { 'id': proj_id, 'title': inp['title'], 'settings': p_sets, 'p_status': inp['p_status'], 'user_id': auth_user_id, 'user_role': user_role }

@errOps.handleExceptions
@secOps.authenticateByToken
async def updateProject(token = '', req = None, proj_id = None, auth_user_id = None):
    inOps.validateId(proj_id)
    inp = await inOps.validateRB(req, { 'title': str, 'settings': str, 'p_status': str, })
    secOps.checkUserPermissionsInProject(auth_user_id, proj_id, min_role='admin')
    p_sets = setsOps.projSets(inp['settings'])
    dbOps.updateExistingProject(proj_id, inp['title'], p_sets, inp['p_status'])
    return { 'proj_id': proj_id, 'proj_title': inp['title'], 'proj_settings': p_sets }

@errOps.handleExceptions
@secOps.authenticateByToken
async def deleteProject(token = '', proj_id = None, auth_user_id = None):
    inOps.validateId(proj_id)
    secOps.checkUserPermissionsInProject(auth_user_id, proj_id, min_role='admin')
    n_rows = dbOps.delProject(proj_id)
    return { 'deleted': n_rows }



@errOps.handleExceptions
@secOps.authenticateByToken
async def getUserProjects(token = '', auth_user_id = None):
    user_projects = dbOps.getUserProjects(auth_user_id)
    resp = { 'projects': [] }
    for p in user_projects:
        if isinstance(p, dict) and \
        all(k in p.keys() for k in ['id', 'title', 'settings', 'user_role']):
            resp['projects'].append({ 
                'id': p['id'], 'title': p['title'], 'settings' : p['settings'],
                'user_role': p['user_role'] } )
    return resp

@errOps.handleExceptions
@secOps.authenticateByToken
async def updateUserProjectMembership(token = '', req = None, auth_user_id = None):
    inp = await inOps.validateRB(req, { 'proj_id': int, 'nick': str, 'user_role': str, })
    secOps.checkUserPermissionsInProject(auth_user_id, inp['proj_id'], min_role='admin')
    new_member_id = dbOps.getUserIdByNick(inp['nick'])
    if not new_member_id:
        raise errOps.BadInputError()
    n_rows = dbOps.addUserToProject(new_member_id, inp['proj_id'], inp['user_role'])
    return { 'user_role': inp['user_role'], 'user_id': new_member_id, 'proj_id': inp['proj_id'], 'changed': n_rows }

@errOps.handleExceptions
@secOps.authenticateByToken
async def deleteUserFromProject(token = '', req = None, auth_user_id = None):
    inp = await inOps.validateRB(req, { 'proj_id': int, 'nick': str, })
    secOps.checkUserPermissionsInProject(auth_user_id, inp['proj_id'], min_role='admin')
    member_id = dbOps.getUserIdByNick(inp['nick'])
    if not member_id:
        raise errOps.BadInputError()
    n_rows = dbOps.delUserFromProject(member_id, inp['proj_id'])
    return { 'deleted': n_rows }



@errOps.handleExceptions
@secOps.authenticateByToken
async def getLabels(token = '', proj_id = None, auth_user_id = None):
    inOps.validateId(proj_id)
    secOps.checkUserPermissionsInProject(auth_user_id, proj_id)
    labels = dbOps.getProjectLabels(proj_id)
    return { 'labels': labels, }

@errOps.handleExceptions
@secOps.authenticateByToken
async def addLabel(token = '', req = None, auth_user_id = None):
    inp = await inOps.validateRB(req, { 'title': str, 'proj_id': int })
    secOps.checkUserPermissionsInProject(auth_user_id, inp['proj_id'])
    label_id = dbOps.labelIDInProject(inp['title'], inp['proj_id'])
    if label_id == None:
        label_id = dbOps.newLabelInProject(inp['title'], inp['proj_id'])
        errOps.validateData(label_id, int)
    resp = { 'id': label_id, 'title': inp['title'], 'proj_id': inp['proj_id'] }
    return resp

@errOps.handleExceptions
@secOps.authenticateByToken
async def renameLabel(token = '', label_id = None, req = None, auth_user_id = None):
    inOps.validateId(label_id)
    inp = await inOps.validateRB(req, { 'new_title': str })
    label_data = dbOps.getLabel(label_id)
    errOps.validateData(label_data, dict, keys=[ 'title', 'project_id'])
    secOps.checkUserPermissionsInProject(auth_user_id, label_data['project_id'], min_role = 'admin')
    n_rows = 0
    if label_data['title'] != inp['new_title']:
        n_rows = dbOps.updateLabel(label_id, inp['new_title'])
    return { 'chagned': n_rows }

@errOps.handleExceptions
@secOps.authenticateByToken
async def delLabel(token = '', label_id = None, auth_user_id = None):
    inOps.validateId(label_id)
    label_data = dbOps.getLabel(label_id)
    errOps.validateData(label_data, dict, keys=[ 'title', 'project_id'])
    secOps.checkUserPermissionsInProject(auth_user_id, label_data['project_id'], min_role = 'admin')
    n_rows = dbOps.deleteLabel(label_id)
    return { 'deleted': n_rows }



@errOps.handleExceptions
@secOps.authenticateByToken
async def getWallets(token = '', proj_id = None, auth_user_id = None):
    inOps.validateId(proj_id)
    secOps.checkUserPermissionsInProject(auth_user_id, proj_id)
    wallets = dbOps.getProjectWallets(proj_id)
    return { 'wallets': wallets }

@errOps.handleExceptions
@secOps.authenticateByToken
async def newWallet(token = '', req = None, auth_user_id = None):
    inp = await inOps.validateRB(req, { 'title': str, 'properties': str, },
                     default_values = { 'value': 0, 'proj_id': None, 'pf_id': None })
    if isinstance(inp['pf_id'], int):
        secOps.checkUserPermissionsInPortfolio(auth_user_id, inp['pf_id'], min_role='admin')
    elif isinstance(inp['proj_id'], int):
        secOps.checkUserPermissionsInProject(auth_user_id, inp['proj_id'], min_role = 'admin')
        pf_props = ''
        inp['pf_id'] = dbOps.newPortfolio(inp['title'], pf_props, inp['proj_id'])
    else:
        raise errOps.BadInputError()
    w_id = dbOps.newWallet(inp['title'], inp['properties'], inp['value'], inp['pf_id'])
    return { 'id': w_id, 'title': inp['title'], 'properties': inp['properties'], 'pf_id': inp['pf_id'], 'pf_properties': pf_props, }

@errOps.handleExceptions
@secOps.authenticateByToken
async def editWallet(token = '', req = None, wallet_id = None, auth_user_id = None):
    inOps.validateId(wallet_id)
    inp = await inOps.validateRB(req, { 'title': str, 'properties': str,},
                     default_values = { 'value': None, 'pf_id': None, })
    secOps.checkUserPermissionsInWallet(auth_user_id, wallet_id, min_role='admin')
    wallet = dbOps.getWallet(wallet_id)
    if inp['value'] == None:
        inp['value'] = wallet['value']
    if inp['pf_id'] == None:
        inp['pf_id'] = wallet['portfolio_id']
    if inp['pf_id'] != wallet['portfolio_id']:
        secOps.checkUserPermissionsInPortfolio(auth_user_id, inp['pf_id'], min_role='admin')
    n_rows = dbOps.editWallet(wallet_id, inp['title'], inp['properties'], inp['value'], inp['pf_id'])
    return { 'id': wallet_id, 'title': inp['title'], 'properties': inp['properties'], 'portfolio_id': inp['pf_id'], 'changed': n_rows }

@errOps.handleExceptions
@secOps.authenticateByToken
async def editPortfolio(token = '', req = None, pf_id = None, auth_user_id = None):
    inOps.validateId(pf_id)
    inp = await inOps.validateRB(req, { 'pf_title': str, 'pf_properties': str, })
    secOps.checkUserPermissionsInPortfolio(auth_user_id, pf_id, min_role='admin')
    n_rows = dbOps.editPortfolio(pf_id, inp['pf_title'], inp['pf_properties'])
    return { 'id': pf_id, 'pf_title': inp['pf_title'], 'pf_properties': inp['pf_properties'], 'portfolio_id': pf_id, 'changed': n_rows }

@errOps.handleExceptions
@secOps.authenticateByToken
async def delWallet(token = '', wallet_id = None, auth_user_id = None):
    inOps.validateId(wallet_id)
    secOps.checkUserPermissionsInWallet(auth_user_id, wallet_id, min_role='admin')
    n_rows = dbOps.delWallet(wallet_id)
    dbOps.cleanWalletlessPortfolios()
    return { 'deleted': n_rows }



@errOps.handleExceptions
@secOps.authenticateByToken
async def getTransactions(token = '', wallet_id = None, auth_user_id = None):
    inOps.validateId(wallet_id)
    secOps.checkUserPermissionsInWallet(auth_user_id, wallet_id)
    transactions = dbOps.getTransactions(wallet_id)
    return { 'transactions': transactions }

@errOps.handleExceptions
@secOps.authenticateByToken
async def newTransaction(token = '', req = None, auth_user_id = None):
    inp = await inOps.validateRB(req, { 'date': str, 'value': int, 'comment': str, },
                       default_values={ 'from_wallet_id': None, 'to_wallet_id': None })
    secOps.checkMoneyTransferPermissions(auth_user_id, [inp['from_wallet_id'], inp['to_wallet_id']])
    tr_id = dbOps.newTransaction(inp['date'], inp['value'], inp['comment'], inp['from_wallet_id'], inp['to_wallet_id'])
    return{ 'id': tr_id, 'date': inp['date'], 'value': inp['value'], 'comment': inp['comment'], 'from_wallet_id': inp['from_wallet_id'], 'to_wallet_id': inp['to_wallet_id'], }

@errOps.handleExceptions
@secOps.authenticateByToken
async def editTransaction(token = '', req = None, tr_id = None, auth_user_id = None):
    inOps.validateId(tr_id)
    inp = await inOps.validateRB(req, { 'date': str, 'comment': str, })
    tr_info = secOps.checkTransactionIntegrity(tr_id)
    secOps.checkTransactionModifyPermissions(auth_user_id, tr_info)
    n_rows = dbOps.editTransaction(inp['date'], inp['comment'], tr_id)
    return { 'id': tr_id, 'value': tr_info['value'], 'from_wallet_id': tr_info['from_wallet_id'], 'to_wallet_id': tr_info['to_wallet_id'], 'date': inp['date'], 'comment': inp['comment'], 'changed': n_rows }

@errOps.handleExceptions
@secOps.authenticateByToken
async def cancelTransaction(token = '', req = None, tr_id = None, auth_user_id = None):
    inOps.validateId(tr_id)
    inp = await inOps.validateRB(req, {}, default_values={ 'rollback': None, })
    tr_info = secOps.checkTransactionIntegrity(tr_id)
    secOps.checkTransactionModifyPermissions(auth_user_id, tr_info)
    if inp['rollback'] != None:
        n_rows = dbOps.rollbackTransaction(tr_id)
    else:
        n_rows = dbOps.deleteTransaction(tr_id)
    return { 'deleted': n_rows, 'rollback': inp['rollback'] != None }



@errOps.handleExceptions
@secOps.authenticateByToken
async def getTransactionsLabelsInProject(token = '', proj_id = None, auth_user_id = None):
    inOps.validateId(proj_id)
    secOps.checkUserPermissionsInProject(auth_user_id, proj_id)
    tr_labels = dbOps.getTransactionsLabelsInProject(proj_id)
    return { 'transaction_labels': tr_labels }

@errOps.handleExceptions
@secOps.authenticateByToken
async def labelTransaction(token = '', req = None, auth_user_id = None):
    inp = await inOps.validateRB(req, { 'label_id': int, 'transaction_id': int, })
    label_data = dbOps.getLabel(inp['label_id'])
    errOps.validateData(label_data, dict, keys=[ 'title', 'project_id'])
    proj_id = label_data['project_id']
    secOps.checkUserPermissionsInProject(auth_user_id, proj_id)
    tr_info = secOps.checkTransactionIntegrity(inp['transaction_id'])
    errOps.validateData(tr_info, dict, keys=[ 'from_wallet_id', 'to_wallet_id'])
    w_from = dbOps.getWallet(tr_info['from_wallet_id'])
    w_to = dbOps.getWallet(tr_info['to_wallet_id'])
    if any(isinstance(w, dict) and 'project_id' in w.keys() and w['project_id'] == proj_id for w in [w_from, w_to]):
        n_rows = dbOps.labelTransaction(inp['label_id'], inp['transaction_id'])
        resp = { 'label_id': inp['label_id'], 'tr_id': inp['transaction_id'], 'changed': n_rows }
    else:
        resp = { 'error': 'Label project has no relaction to transaction projects' }
    return resp

@errOps.handleExceptions
@secOps.authenticateByToken
async def unLabelTransaction(token = '', req = None, auth_user_id = None):
    inp = await inOps.validateRB(req, { 'label_id': int, 'transaction_id': int, })
    label_data = dbOps.getLabel(inp['label_id'])
    errOps.validateData(label_data, dict, keys=[ 'title', 'project_id'])
    proj_id = label_data['project_id']
    secOps.checkUserPermissionsInProject(auth_user_id, proj_id)
    n_rows = dbOps.unLabelTransaction(inp['label_id'], inp['transaction_id'])
    return { 'deleted': n_rows }



@errOps.handleExceptions
@secOps.authenticateByToken
async def getSchedules(token = '', proj_id = None, auth_user_id = None):
    inOps.validateId(proj_id)
    secOps.checkUserPermissionsInProject(auth_user_id, proj_id)
    schedules = dbOps.getProjectSchedules(proj_id)
    return { 'schedules': schedules }

@errOps.handleExceptions
@secOps.authenticateByToken
async def newSchedule(token = '', req = None, auth_user_id = None):
    inp = await inOps.validateRB(req, { 'comment': str, 'date': str, 'repeat': str, 'tz_offset_min': int,
                                        'value': int, 'percent': int },
                       default_values={ 'from_wallet_id': None, 'to_wallet_id': None })
    secOps.checkMoneyTransferPermissions(auth_user_id, [inp['from_wallet_id'], inp['to_wallet_id']])
    is_percent = bool(inp['percent'])
    sc_id = dbOps.newSchedule(inp['comment'], inp['date'], inp['tz_offset_min'], inp['repeat'], inp['value'], is_percent, inp['from_wallet_id'], inp['to_wallet_id'])
    return{ 'id': sc_id, 'comment': inp['comment'], 'date': inp['date'], 'tz_offset_min': inp['tz_offset_min'], 'repeat': inp['repeat'], 'value': inp['value'], 'is_percent': is_percent, 'from_wallet_id': inp['from_wallet_id'], 'to_wallet_id': inp['to_wallet_id'], }

@errOps.handleExceptions
@secOps.authenticateByToken
async def editSchedule(token = '', req = None, sc_id = None, auth_user_id = None):
    inOps.validateId(sc_id)
    inp = await inOps.validateRB(req, { 'comment': str, 'date': str, 'repeat': str, 'tz_offset_min': int,
                                        'value': int, 'percent': int })
    sc_info = secOps.checkScheduleIntegrity(sc_id)
    secOps.checkScheduleModifyPermissions(auth_user_id, sc_info)
    is_percent = bool(inp['percent'])
    n_rows = dbOps.editSchedule(inp['comment'], inp['date'], inp['tz_offset_min'], inp['repeat'], inp['value'], is_percent, sc_id)
    return { 'id': sc_id, 'comment': inp['comment'], 'date': inp['date'], 'tz_offset_min': inp['tz_offset_min'], 'repeat': inp['repeat'], 'value': inp['value'], 'from_wallet_id': sc_info['from_wallet_id'], 'to_wallet_id': sc_info['to_wallet_id'], 'changed': n_rows }

@errOps.handleExceptions
@secOps.authenticateByToken
async def deleteSchedule(token = '', sc_id = None, auth_user_id = None):
    inOps.validateId(sc_id)
    sc_info = secOps.checkScheduleIntegrity(sc_id)
    secOps.checkScheduleModifyPermissions(auth_user_id, sc_info)
    n_rows = dbOps.deleteSchedule(sc_id)
    return { 'deleted': n_rows }



@errOps.handleExceptions
@secOps.authenticateByToken
async def getSchedulesLabelsInProject(token = '', proj_id = None, auth_user_id = None):
    inOps.validateId(proj_id)
    secOps.checkUserPermissionsInProject(auth_user_id, proj_id)
    tr_labels = dbOps.getSchedulesLabelsInProject(proj_id)
    return { 'schedule_labels': tr_labels }

@errOps.handleExceptions
@secOps.authenticateByToken
async def labelSchedule(token = '', req = None, auth_user_id = None):
    inp = await inOps.validateRB(req, { 'label_id': int, 'schedule_id': int, })
    label_data = dbOps.getLabel(inp['label_id'])
    errOps.validateData(label_data, dict, keys=[ 'title', 'project_id'])
    proj_id = label_data['project_id']
    secOps.checkUserPermissionsInProject(auth_user_id, proj_id)
    tr_info = secOps.checkScheduleIntegrity(inp['schedule_id'])
    errOps.validateData(tr_info, dict, keys=[ 'from_wallet_id', 'to_wallet_id'])
    w_from = dbOps.getWallet(tr_info['from_wallet_id'])
    w_to = dbOps.getWallet(tr_info['to_wallet_id'])
    if any(isinstance(w, dict) and 'project_id' in w.keys() and w['project_id'] == proj_id for w in [w_from, w_to]):
        n_rows = dbOps.labelSchedule(inp['label_id'], inp['schedule_id'])
        resp = { 'label_id': inp['label_id'], 'tr_id': inp['schedule_id'], 'changed': n_rows }
    else:
        resp = { 'error': 'Label project has no relaction to schedule projects' }
    return resp

@errOps.handleExceptions
@secOps.authenticateByToken
async def unLabelSchedule(token = '', req = None, auth_user_id = None):
    inp = await inOps.validateRB(req, { 'label_id': int, 'schedule_id': int, })
    label_data = dbOps.getLabel(inp['label_id'])
    errOps.validateData(label_data, dict, keys=[ 'title', 'project_id'])
    proj_id = label_data['project_id']
    secOps.checkUserPermissionsInProject(auth_user_id, proj_id)
    n_rows = dbOps.unLabelSchedule(inp['label_id'], inp['schedule_id'])
    return { 'deleted': n_rows }







