from fastapi import FastAPI
from routes.route import router
from prometheus_client import start_http_server
import uvicorn

app = FastAPI()
app.include_router(router)

def main():
    start_http_server(8000)
    uvicorn.run(app, host="0.0.0.0", port=8001)

if __name__ == "__main__":
    main()
