from fastapi import Request, APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from typing import Optional

import ops_api as apiOps

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')



@router.get('/user/{nik}')
async def getUserInfo(nik, tok = Depends(oauth2_scheme)):
    return await apiOps.getUserInfo(token = tok, nick = nik)

@router.post('/user')
async def registerNewUser(r: Request):
    return await apiOps.registerNewUser(req = r)

@router.put('/user')
async def updateUserInfo(r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.updateUserInfo(token = tok, req = r)

@router.delete('/user')
async def deleteUser(r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.deleteUser(token = tok, req = r)



@router.post('/project')
async def newProject(r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.newProject(token = tok, req = r)

@router.put('/project/{id}')
async def updateProject(id: int, r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.updateProject(token = tok, req = r, proj_id = id)

@router.delete('/project/{id}')
async def deleteProject(id: int, tok = Depends(oauth2_scheme)):
    return await apiOps.deleteProject(token = tok, proj_id = id)



@router.get('/userprojects')
async def getUserProjects(tok = Depends(oauth2_scheme)):
    return await apiOps.getUserProjects(token = tok)

@router.post('/userproject')
async def updateUserProjectMembership(r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.updateUserProjectMembership(token = tok, req = r)

@router.delete('/userproject')
async def deleteUserProjectMembership(r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.deleteUserFromProject(token = tok, req = r)



@router.get('/devices')
async def getDevices(tok = Depends(oauth2_scheme)):
    return await apiOps.getDevices(token = tok)

@router.post('/device')
async def addDeviceWithPassword(r: Request):
    return await apiOps.addDeviceWithPassword(req = r)

@router.put('/device/{id}')
async def updateDeviceInfo(id: int, r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.updateDeviceInfo(token = tok, req = r, device_id = id)

@router.delete('/device/{id}')
async def deleteDevice(id: int, tok = Depends(oauth2_scheme)):
    return await apiOps.deleteDevice(token = tok, device_id = id)

@router.delete('/device')
async def deleteDevice(tok = Depends(oauth2_scheme)):
    return await apiOps.deleteDevice(token = tok)


@router.get('/labels/{proj_id}')
async def getLabels(proj_id: int, tok = Depends(oauth2_scheme)):
    return await apiOps.getLabels(token = tok, proj_id = proj_id)

@router.post('/label')
async def addLabel(r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.addLabel(token = tok, req = r)

@router.put('/label/{id}')
async def renameLabel(id: int, r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.renameLabel(token = tok, req = r, label_id = id)

@router.delete('/label/{id}')
async def delLabel(id: int, tok = Depends(oauth2_scheme)):
    return await apiOps.delLabel(token = tok, label_id = id)



@router.get('/wallets/{proj_id}')
async def getWallets(proj_id: int, tok = Depends(oauth2_scheme)):
    return await apiOps.getWallets(proj_id = proj_id, token = tok)

@router.post('/wallet')
async def newWallet(r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.newWallet(token = tok, req = r)

@router.put('/wallet/{id}')
async def editWallet(id: int, r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.editWallet(token = tok, req = r, wallet_id = id)

@router.put('/portfolio/{id}')
async def editPortfolio(id: int, r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.editPortfolio(token = tok, req = r, pf_id = id)

@router.delete('/wallet/{id}')
async def delWallet(id: int, tok = Depends(oauth2_scheme)):
    return await apiOps.delWallet(token = tok, wallet_id = id)




@router.get('/transactions/{wallet_id}')
async def getTransactions(wallet_id: int, tok = Depends(oauth2_scheme)):
    return await apiOps.getTransactions(wallet_id = wallet_id, token = tok)

@router.post('/transaction')
async def newTransaction(r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.newTransaction(token = tok, req = r)

@router.put('/transaction/{id}')
async def editTransaction(id: int, r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.editTransaction(token = tok, req = r, tr_id = id)

@router.delete('/transaction/{id}')
async def cancelTransaction(id: int, r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.cancelTransaction(token = tok, req = r, tr_id = id)



@router.get('/transactionlabels/{proj_id}')
async def getTransactionsLabelsInProject(proj_id: int, tok = Depends(oauth2_scheme)):
    return await apiOps.getTransactionsLabelsInProject(proj_id = proj_id, token = tok)

@router.post('/transactionlabel')
async def labelTransaction(r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.labelTransaction(token = tok, req = r)

@router.delete('/transactionlabel')
async def unLabelTransaction(r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.unLabelTransaction(token = tok, req = r)



@router.get('/schedules/{proj_id}')
async def getSchedules(proj_id: int, tok = Depends(oauth2_scheme)):
    return await apiOps.getSchedules(proj_id = proj_id, token = tok)

@router.post('/schedule')
async def newSchedule(r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.newSchedule(token = tok, req = r)

@router.put('/schedule/{id}')
async def editSchedule(id: int, r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.editSchedule(token = tok, req = r, sc_id = id)

@router.delete('/schedule/{id}')
async def deleteSchedule(id: int, tok = Depends(oauth2_scheme)):
    return await apiOps.deleteSchedule(token = tok, sc_id = id)



@router.get('/schedulelabels/{proj_id}')
async def getSchedulesLabelsInProject(proj_id: int, tok = Depends(oauth2_scheme)):
    return await apiOps.getSchedulesLabelsInProject(proj_id = proj_id, token = tok)

@router.post('/schedulelabel')
async def labelSchedule(r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.labelSchedule(token = tok, req = r)

@router.delete('/schedulelabel')
async def unLabelSchedule(r: Request, tok = Depends(oauth2_scheme)):
    return await apiOps.unLabelSchedule(token = tok, req = r)
