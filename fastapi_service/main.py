import fastapi

import routers.io


app: fastapi.FastAPI = fastapi.FastAPI()


@app.middleware("http")
async def log_real_ip(request: fastapi.Request, call_next):
    client_host = request.headers.get("X-Forwarded-For", request.client.host)
    print(f"Client real IP: {client_host}")
    response = await call_next(request)
    return response

app.include_router(routers.io.router)
