import fastapi

import routers.io


app: fastapi.FastAPI = fastapi.FastAPI()
app.include_router(routers.io.router)
