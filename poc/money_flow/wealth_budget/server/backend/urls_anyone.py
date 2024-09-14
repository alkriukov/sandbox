from fastapi import APIRouter

import ops_db as dbOps
import ops_input as inOps

router = APIRouter()

@router.get("/")
async def heartBeat():
    return {"state": "Active"}

@router.get("/ck/{nick}")
async def isUserNameOccupied(nick):
    if inOps.validateNick(nick):
        resp = {"occupied": str(dbOps.isUserInDb(nick))}
    else:
        resp = ""
    return resp
