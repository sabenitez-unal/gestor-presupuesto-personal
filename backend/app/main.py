from fastapi import FastAPI

app =  FastAPI()

@app.get("/")
def read_root():
    return {"mensaje" : "Guten Morgen!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"ItemID" : item_id}