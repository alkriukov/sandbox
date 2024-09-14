from fastapi import FastAPI
import uvicorn

import urls_anyone
import urls_user

app = FastAPI()
app.include_router(urls_anyone.router)
app.include_router(urls_user.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)

