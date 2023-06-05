import fastapi
from fastapi import FastAPI
from fastapi.params import Body
from fastapi.params import Optional
from pydantic import BaseModel
from random import randrange

app = FastAPI()


# STORES ALL THE POSTS
my_posts = [{"titile": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite shoes", "content": "New Balances", "id": 2}]

def find_post(id):
    for posts in my_posts:
        if posts['id'] == id:
            return posts


class Post(BaseModel):
    title: str
    content: str
    publishhed: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    print()
    print(my_posts)
    return {"data": my_posts}

@app.post("/posts")
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0, 100000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    print(post)
    return {"post_detail": post}



# TITLE STR, CONTENT STR, 
