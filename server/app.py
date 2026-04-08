from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.api_route("/reset", methods=["GET", "POST"])
def reset():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "running"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()