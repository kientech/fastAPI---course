from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content:  str
    published: bool = True


while True:
    try:
        connect = psycopg2.connect(host='localhost', database='fastAPI', user='postgres',
                                   password='kienduongtrung0406', cursor_factory=RealDictCursor)
        cursor = connect.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print('Coonnection to database failed')
        print(error)
        time.sleep(2)
my_posts = [
    {
        "title": "Title of post 1",
        "content": "Content of post 1",
        "id": 1
    },
    {
        "title": "Title of post 2",
        "content": "Content of post 2",
        "id": 2
    },
]


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post


def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index


@app.get("/")
def root():
    return {"name": "Welcome to my FastAPI"}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"posts": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 10000000)
    # my_posts.append(post_dict)
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    connect.commit()
    return {"data": new_post}

# @app.get("posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     return {"post_details": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post {} not found".format(id))
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post {} not found".format(id)}
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}
