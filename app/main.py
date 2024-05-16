from typing import Optional , List
from fastapi import FastAPI , Response , status , HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def main():
    return {"message": "Hello World"}

# Import Routers
from .routers import post, user , auth , vote



#database driver install package
import psycopg
#import psycopg.extras import RealDictCursor

#Import ORM models and Engines
from  . import models , utils
from .database import engine, get_db

#Request schemase

from . import schemas
from .config import settings


# This is the sql alchemy model engine before we used alembic
# models.Base.metadata.create_all(bind=engine)





app = FastAPI()

#Router setups
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")
async def root():
    return {"message": "Hello World"}



# # Testing sqlalchmey route
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}







    



    

