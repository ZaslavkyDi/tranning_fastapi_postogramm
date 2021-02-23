import uvicorn
from fastapi.applications import FastAPI

from app.api import users

app = FastAPI()

app.include_router(router=users.router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
