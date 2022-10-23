from email.policy import strict
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content:str
    published: bool = True
    rating: Optional[int] = None

my_post = [{"title":"title of post 1", "content": "content of post 1","id": 1},{"title":"comida", "content": "comidas que eu gosto","id": 2}]
    
@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_post}

@app.post("/posts")
def create_posts(post: Post):
    #print(post)
    #print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_post.append(post_dict)
    return {"data":post_dict}

