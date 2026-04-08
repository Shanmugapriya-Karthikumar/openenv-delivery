from fastapi import FastAPI

app = FastAPI()

@app.api_route("/reset", methods=["GET", "POST"])
def reset():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "running"}
