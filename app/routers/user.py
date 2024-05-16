
from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session


import psycopg

#Import ORM models and Engines
from  .. import models , schemas, utils
from ..database import  get_db


router = APIRouter(
    prefix="/v1/users",
    tags=['Users']
)


# Create User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        #hass the password from user.password
        hashed_password = utils.hass_password(user.password)
        user.password = hashed_password
        #print(**user.model_dump())
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return  new_user
    except Exception as e:
        print(e)
        return  e


# Get User By UserID

@router.get("/{id}", response_model = schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    return db_user