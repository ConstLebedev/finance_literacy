from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from db.database import db_conn_str
from routes import auth, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome To"}


register_tortoise(
    app,
    db_url=db_conn_str,
    modules={"models": ["db.models"]},
    generate_schemas=True,  # dev
    add_exception_handlers=True,  # dev
)

