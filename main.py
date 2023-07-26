from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from app.server.routes.api import router as api_router
from app.server.routes import root
from app.server.core.config import API_PREFIX, PROJECT_NAME

# if __name__ == "__main__":
#     uvicorn.run("server.app:app", host="localhost", port=8001, reload=True)


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, docs_url="/docs", openapi_url="/openapi.json")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(api_router, prefix=API_PREFIX)
    application.include_router(root.router, tags=["root"], prefix="")

    return application


app = get_application()

if __name__ == '__main__':
    from uvicorn import run
    run(app)