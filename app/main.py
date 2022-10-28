from email.policy import strict
from fastapi import FastAPI, Response, status , HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
import sqlalchemy.dialects.postgresql 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class Post(BaseModel):
    title: str
    content:str
    published: bool = True
   #rating: Optional[int] = None

while True:
    
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='nuvem', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)

my_post = [{"title":"title of post 1", "content": "content of post 1","id": 1},{"title":"comida", "content": "comidas que eu gosto","id": 2}]
 
def find_post(id):
    for p in my_post:
        if p["id"] ==id:
            return p
    
def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i  
          
@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}
    

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    return {'data': updated_post}