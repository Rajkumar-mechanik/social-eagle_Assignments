from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "message": "Hello, Social Eagle's squad! Welcome to the FastAPI application."
    }


@app.get("/greet/{name}")
def greet(name: str):
    return {
        "message": f"Hello, {name}"
    }
