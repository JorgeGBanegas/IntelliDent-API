from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Bienvenido a IntelliDent API",
        "version": "1.0.0",
        "author": "Jorge Gustavo Banegas Melgar",
        "email": "jorge.g.banegas@gmail.com"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
