import json
from fastapi import Request

import ops_err as errOps

async def validateRB(r: Request, expect_fields_types: dict, default_values: dict= {}):
    rb = await r.body()
    retJson = {}
    rJ = json.loads(rb.decode('utf-8', errors='ignore'))
    if isinstance(rJ, dict):
        for field in expect_fields_types.keys():
            if field in rJ.keys() and isinstance(rJ[field], expect_fields_types[field]):
                validateField(field, rJ[field])
                retJson[field] = rJ[field]
            else:
                print(rJ.keys(), 'should have', field, 'with type of', expect_fields_types[field])
                raise errOps.BadInputError()
        for field in default_values.keys():
            if field in rJ.keys():
                validateField(field, rJ[field])
                retJson[field] = rJ[field]
            else:
                retJson[field] = default_values[field]
    else:
        print(rJ, 'is not a dictionary. Raising BadInputError')
        raise errOps.BadInputError()
    return retJson

def validateNick(nick):
    if False:
        raise errOps.BadInputError()
    return True

def validateId(id, allow_none = False):
    if False:
        raise errOps.BadInputError()
    return True

def validateField(field_name, value):
    match field_name:
        case 'id' | 'proj_id' :
            validateId(value)
        case 'nick':
            validateNick(value)
        case 'passwd' | 'cur_passwd' | 'new_passwd':
            if False:
                raise errOps.BadInputError()
        case 'settings' | 'new_settings':
            if False:
                raise errOps.BadInputError()
        case 'device_info':
            if False:
                raise errOps.BadInputError()
        case 'token':
            if False:
                raise errOps.BadInputError()
        case 'title':
            if False:
                raise errOps.BadInputError()
        case 'user_role':
            if False:
                raise errOps.BadInputError()
        case 'm_status':
            if False:
                raise errOps.BadInputError()
        case _:
            print('WARNING: no input validation suppprt for', field_name)
    return True
