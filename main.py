from fastapi import FastAPI,Response, status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time

app = FastAPI()

class post(BaseModel):
    title: str
    content: Optional[str]=None
    published: bool=True
    rating: Optional[int]=None

while True:
    try:
        conn= psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='1234',cursor_factory=RealDictCursor)
        cursor =conn.cursor()
        print("database connection was sucessful")
        break
    except Exception as error:
        print("database connection was failed")
        print("Error: ",error)
        time.sleep(3)

my_posts = [{"Title": "title of post 1", "content": "content of post 1", "id": 1}, { "Title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i
        

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/posts")
def get_post():
    cursor.execute(""" SELECT * FROM posts """)
    posts= cursor.fetchall()
    print(posts)
    return {"data": my_posts}

@app.post("/posts")
def create_post(post: post):
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    (post.title,post.content,post.published))

    new_post=cursor.fetchone()

    # without commit no changes can made in database
    conn.commit()

    return {"Message": new_post}

""" @app.post("/createposts")
def get_post(payLoad: dict = Body(...)):
    print(payLoad)
    return {"Message": f"Successfully Created the post {payLoad['Title']}"} """

""" @app.post("/createposts")
def get_post(new_post:post):
    print(new_post.rating)
    print(new_post.dict())
    return {"data": "new post"} """

""" @app.post("/posts")
def get_post(post:post):
    print(post.rating)
    print(post.dict())
    return {"data": "new post"} """

@app.post("/posts")
def get_post(post:post):
    post_dict =post.dict()
    post_dict['id']=randrange(0,10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id:str):
    cursor.execute(""" SELECT * FROM posts Where id=%s """,(str(id)))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with {id} was not found here')
    return {"post_detail": post}
    
""" @app.get("/posts/{id}")
def get_post(id):
    print(id)
    return {"post_detail": f"Here is post {id}"} """

#if other than number is given to postman after "posts/oimn" we can't know what is wrong best is way is just down 
""" @app.get("/posts/{id}")
def get_post(id):
    post=find_post(int(id))
    print(post)
    return {"post_detail": post}
 """

@app.get("/posts/latest") 
def get_latest_post():
    post = my_posts [len (my_posts)-1]
    return {"detail": post}

 #best way to know the mistake
""" @app.get("/posts/{id}")
def get_post(id:int,response:Response):

    post=find_post(id)
    print(post)
    if not post:
        #response.status_code=404
        response.status_code=status.HTTP_404_NOT_FOUND
        return{'message':f'post with {id} was not found'}
    return {"post_detail": post} """

@app.get("/posts/{id}")
def get_post(id:int):

    post=find_post(id)
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with {id} was not found here')
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(id),)) 
    deleted_post = cursor.fetchone() 
    conn.commit()
    if deleted_post == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f" post with id: {id} does not exist")
    return Response (status_code=status.HTTP_204_NO_CONTENT)

""" @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required ID
    #my_posts.pop(index)
    index = find_index_post(id)
    my_posts.pop(index)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with {id} does not exist')
    #return {"message": "post was succesfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 """

@app.put("/posts/{id}") 
def update_post(id: int, post: post):
    cursor.execute("""UPDATE posts SET title=%s, content = %s, published = %s WHERE id = %s RETURNING *""",
     (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return {"data": updated_post}

""" @app.put("/posts/{id}")
def update_post(id:int, post:post):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with {id} does not exist')
    
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict

    return{'message':"updated post"} """
