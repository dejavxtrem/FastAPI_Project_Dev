
from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter 
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from fastapi.encoders import jsonable_encoder

#database driver install package
import psycopg

#Import ORM models and Engines
from  .. import models , schemas, utils , oauth2
from ..database import  get_db



#Router path prefix
router = APIRouter(
    prefix="/v1/posts",
    tags=['Posts']
)





#Get all Posts
#Limit  Query parameter = 10 the query parameter
#Skip Query parameters =0
#Setting up pagination on the frontend using offset and pagination
#Search query parameter
@router.get("/" , response_model = list[schemas.PostVoteResponse])
# @router.get("/" )
def get_posts( db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user),
        Limit: int = 10,
        Skip: int = 0,
        search:  Optional[str] = ""
        ):
    try:
        print(Limit)
        # use a filter to compare the  current id of the user with the  post owner id
        #posts = db.query(models.Post).filter(models.post.owner_id === current_user.id).all

        #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(Skip).all()

         #Performing a join on a sql archemy with you different models (by default it set out innter join)
        posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(Skip).all()

        

        return posts
    except Exception as e:
        print(e)
        return  e 
  
#
#create post
@router.post("/", status_code=status.HTTP_201_CREATED , response_model = schemas.PostResponse )
def create_posts(post: schemas.PostCreate , db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    try:
        #print(**post.model_dump())
        #print(f"this is current user {current_user.id}")
        new_post = models.Post(owner_id = current_user.id, **post.model_dump())

        print(new_post)

        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return  new_post
    except Exception as e:
        print(e)
        return e

        
# Get one post
@router.get("/{id}", response_model = schemas.PostVoteResponse)
def get_post(id: int , db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    try:
        # post = db.query(models.Post).filter(models.Post.id == id).first()

        post = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
        
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
        
        return  post 
    except Exception as e:
        print(e)
        return  e






# Delete Post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int ,  db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    try:
        delete_post = db.query(models.Post).filter(models.Post.id == id)

        post = delete_post.first()

        if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
        
        if post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        
        delete_post.delete(synchronize_session=False)

        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        print(e)
        return  e
 


#update Post

@router.put("/{id}",  response_model = schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate , db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    try:
        update_post = db.query(models.Post).filter(models.Post.id == id)

        post_query = update_post.first()
        
        
        if post_query == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
        
        if post_query.owner_id != current_user.id:

            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

        
        jsondata = jsonable_encoder(post.model_dump())

        #print(f"this is the data {jsondata}")

        update_post.update(post.model_dump(), synchronize_session=False)
        db.commit()
        return  update_post.first()
    except Exception as e:
        print(e)
        return  e
    




