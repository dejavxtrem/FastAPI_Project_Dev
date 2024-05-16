from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from . import schemas , database , models
from fastapi import Depends , status , HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

#Endpoint of our authentication and token
auth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = f'{settings.secret_key}'
ALGORITHM = f'{settings.algorithm}'
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict , expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # JWT function to encode the data and add algo and expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


# Authorization function dependency
def get_current_user(token: str = Depends(auth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
            detail= f"could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
    )
    print(f'working with the call')
    # Fetch User from Database
    token = verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    print(user)
    return user