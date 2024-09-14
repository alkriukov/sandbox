from hashlib import sha512

import ops_db as dbOps
import ops_input as inOps
import ops_err as errOps

def authenticateByToken(func):
    async def wrapper(*args, **kwargs):
        tok = kwargs.get('token', None)
        user_id = authenticate(token = tok)
        if not isinstance(user_id, int):
             raise errOps.AuthenticationError()
        resp = await func(*args, **kwargs, auth_user_id = user_id)
        return resp
    return wrapper

def newToken(nick_v):
    print('WARNING: TOKEN GENERATION IS INSECURE')
    return nick_v

def getToken(raw_token):
    return sha512(str(raw_token).encode('utf-8', errors='ignore')).hexdigest()

def getPasswd(passwd, reg_dt_v):
    salt = str(reg_dt_v) + ', '
    pass_base = salt + passwd
    return sha512(str(pass_base).encode('utf-8', errors='ignore')).hexdigest()

def authenticate(token = None):
    if token == None:
        raise errOps.AuthenticationError()
    inOps.validateField("token", token)
    user_id_data = dbOps.getUserIdByDeviceToken(getToken(token))
    if not isinstance(user_id_data, dict) or "user_id" not in user_id_data.keys():
        raise errOps.AuthenticationError()
    user_id = user_id_data["user_id"]
    if not isinstance(user_id, int):
        raise errOps.AuthenticationError()
    return user_id

def getCompatibleRolesMyMinimalRequiredRole(role):
    roles = (role,)
    match role:
        case 'member':
            roles = (role, 'admin')
        case _:
            pass
    return roles

def hasUserRoleInProject(auth_user_id_v, project_id_v, min_role='member'):
    res = False
    roles = getCompatibleRolesMyMinimalRequiredRole(min_role)
    if dbOps.getUserRoleInProject(auth_user_id_v, project_id_v) in roles:
        res = True
    return res

def checkUserPermissionsInProject(auth_user_id_v, project_id_v, min_role='member'):
    if not hasUserRoleInProject(auth_user_id_v, project_id_v, min_role=min_role):
        raise errOps.AuthorizationError()
    return True

def checkUserPermissionsInPortfolio(auth_user_id_v, port_id_v, min_role='member'):
    portfolio = dbOps.getPortfolio(port_id_v)
    if not isinstance(portfolio, dict) or 'project_id' not in portfolio.keys():
        raise errOps.AuthorizationError()
    checkUserPermissionsInProject(auth_user_id_v, portfolio['project_id'], min_role=min_role)
    return True

def checkUserPermissionsInWallet(auth_user_id_v, wallet_id_v, min_role='member'):
    wallet = dbOps.getWallet(wallet_id_v)
    if not isinstance(wallet, dict) or 'project_id' not in wallet.keys():
        raise errOps.AuthorizationError()
    checkUserPermissionsInProject(auth_user_id_v, wallet['project_id'], min_role=min_role)
    return True

def checkMoneyTransferPermissions(auth_user_id_v, wallet_ids_v):
    for wallet_id in wallet_ids_v:
        if wallet_id != None:
            wallet = dbOps.getWallet(wallet_id)
            if not isinstance(wallet, dict) or 'project_id' not in wallet.keys():
                raise errOps.AuthorizationError()
            if not dbOps.getUserRoleInProject(auth_user_id_v, wallet['project_id']):
                raise errOps.AuthorizationError()
    return True

def checkTransactionIntegrity(tr_id_v):
    tr_info = dbOps.getTransaction(tr_id_v)
    errOps.validateData(tr_info, dict, ['date', 'value', 'comment', 'from_wallet_id', 'to_wallet_id'])
    return tr_info

def checkTransactionModifyPermissions(auth_user_id_v, tr_info_v):
    checkMoneyTransferPermissions(auth_user_id_v, [tr_info_v['from_wallet_id'], tr_info_v['to_wallet_id']])

def checkScheduleIntegrity(sc_id_v):
    sc_info = dbOps.getSchedule(sc_id_v)
    errOps.validateData(sc_info, dict, ['comment', 'next_date', 'repeat_rule', 'value', 'value_is_percent', 'from_wallet_id', 'to_wallet_id'])
    return sc_info

def checkScheduleModifyPermissions(auth_user_id_v, sc_info_v):
    checkMoneyTransferPermissions(auth_user_id_v, [sc_info_v['from_wallet_id'], sc_info_v['to_wallet_id']])
