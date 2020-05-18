from fastapi import FastAPI, HTTPException
app = FastAPI()

from pydantic import BaseModel

class Name(BaseModel):
    who:str

@app.post("/")
def say_hello(item:Name):
    return {"rsps":item.who}
