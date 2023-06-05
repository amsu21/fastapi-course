import fastapi
from fastapi import FastAPI, HTTPException, Response, status
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

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0, 100000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_400_BAD_REQUEST
        # return {'message': f"post with id: {id} was not found"}
    print(post)
    return {"post_detail": post}



# TITLE STR, CONTENT STR, 
