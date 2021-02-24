import uvicorn
from fastapi.applications import FastAPI
from fastapi_jwt_auth.auth_jwt import AuthJWT

from app.api import users
from app.core.config import settings

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return settings


app.include_router(router=users.router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
