from fastapi import FastAPI

app = FastAPI()


@app.get("/alive")
async def get_alive():
    return
