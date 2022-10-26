from email.policy import strict
from fastapi import FastAPI, Response, status , HTTPException
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

@app.get("/posts")
def get_posts():
    return {"data": my_post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_post.append(post_dict)
    return {"data":post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #find the index in the array that hand required id
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    post_dict = post.dict()
    post_dict["id"] = id
    my_post[index] = post_dict
    return {'data': post_dict}