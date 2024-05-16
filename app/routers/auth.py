from fastapi import APIRouter , Response , status , HTTPException , Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..database import  get_db
from ..import schemas, models, utils , oauth2

router = APIRouter(
    prefix="/v1/auth",
    tags=['Authentication']
)



@router.post('/login', response_model=schemas.Token , status_code=status.HTTP_200_OK)
# Dependecy OAuth2PasswordRequestForm
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    try:

        user_account = db.query(models.User).filter(models.User.email == user_credentials.username).first()
        if not user_account:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        
        if not utils.compare_password(user_credentials.password, user_account.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        

        access_token = oauth2.create_access_token(data={"user_id": user_account.id})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        return e

