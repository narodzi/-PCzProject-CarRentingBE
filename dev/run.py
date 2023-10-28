import uvicorn

if __name__ == "__main__":
    from main import app
    uvicorn.run(app, host="0.0.0.0", port=4300)
