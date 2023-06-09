import fastapi
from fastapi import FastAPI, HTTPException, Response, status
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.params import Body
from fastapi.params import Optional
from pydantic import BaseModel
from random import randrange
import time

app = FastAPI()

# STORES ALL THE POSTS
my_posts = [{"titile": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite shoes", "content": "New Balances", "id": 2}]

while True:
    
    # DATABASE CONNECTION
    try:
        connect = psycopg2.connect(host = 'localhost', database = 'fastapi', user='postgres', password='rootroot', cursor_factory=RealDictCursor)
        cursor = connect.cursor()
        print()
        print("DATABASE CONNECTED!!!")
        print()
        break
    except Exception as error:
        print("IT AINT WORK DAWG")
        print()
        print("Error was: ", error)
        time.sleep(2)


def find_post(id):
    for posts in my_posts:
        if posts['id'] == id:
            return posts
        
def find_index_post(id):
    for index, posts in enumerate(my_posts):
        if posts['id'] == id:
            return index
        

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    id: int
    created_at: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

# GET POSTS
@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print()
    print("GOT YOUR POSTS!!!!!!!")
    print()
    return {"data": posts}

# CREATE POSTS
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    # INSERTING POSTS INTO THE DATABASE
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (new_post.title, new_post.content, new_post.published))
    created_post = cursor.fetchone()
    return {"data": created_post}


# GET SPECIFIC POST
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_400_BAD_REQUEST
        # return {'message': f"post with id: {id} was not found"}
    print(post)
    return {"post_detail": post}


# DELETE A POST
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # FIND THE INDEX IN THE ARRAY THAT HAS REQUIRED ID
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE POST
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # FIND THE INDEX IN THE ARRAY THAT HAS REQUIRED ID
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    print()
    print(post)
    print()
    return {'data': post_dict}
