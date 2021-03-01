import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi_jwt_auth import AuthJWT

from app.api import users, auth, posts
from app.core.config import settings

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return settings


app.include_router(router=auth.router, prefix='/auth', )
app.include_router(router=users.router, prefix='/users', )
app.include_router(router=posts.router, prefix='/posts', )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )

    # Custom documentation fastapi-jwt-auth
    headers = {
        "name": "Authorization",
        "in": "header",
        "required": True,
        "schema": {
            "title": "Authorization",
            "type": "string"
        },
    }

    # Get routes from index 4 because before that fastapi define router for /openapi.json, /redoc, /docs, etc
    # Get all router where operation_id is authorize
    router_authorize = [route for route in app.routes[4:] if route.operation_id == "authorize"]

    for route in router_authorize:
        method = list(route.methods)[0].lower()
        try:
            # If the router has another parameter
            openapi_schema["paths"][route.path][method]['parameters'].append(headers)
        except Exception:
            # If the router doesn't have a parameter
            openapi_schema["paths"][route.path][method].update({"parameters": [headers]})

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
