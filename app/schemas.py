#Define a class to define how the post will look like in a request and response
from pydantic import BaseModel , EmailStr
from datetime import datetime
from typing import Optional

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# User Response Schema pydantic model
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

# Post bAse class for extending
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    owner:UserResponse  # creates the one to many relationshp
    



# Request Schema pydantic model
class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True


class PostUpdate(PostBase):
    owner_id: Optional[int] = None


# Response Schema pydantic model
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    
    class Config:
        from_attributes = True


# Post vote Response after table join
class PostVoteResponse(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True
        





class PostUpdateResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    title: str
    content: str
    published: bool = True

    class Config:
        from_attributes = True



# User Schema pydantic model
class UserCreate(BaseModel):
    email: EmailStr
    password: str






class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class VoteCreate(BaseModel):
    post_id: int
    dir: int

