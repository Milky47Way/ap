from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def index():
    return "Hello FastAPI!"

@app.get("/carrot")
def carrot():
    return <b>"Wow Carrot!"</b>
