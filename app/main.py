from urllib.request import Request

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.v1.routes import routers as v1_routers
from app.core.config import settings
from app.core.container import Container
from app.utils.class_object import singleton


@singleton
class App:
    def __init__(self):
        # Initialize the app
        self.app = FastAPI(
            title=settings.PROJECT_NAME,
            openapi_url=f"{settings.API_V1_STR}/openapi.json",
            version="2.1.0"
        )

        self.container = Container()
        self.db = self.container.db()

        if settings.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=settings.BACKEND_CORS_ORIGINS,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        @self.app.get("/")
        def root():
            return {"message": "Welcome to the FastAPI application!"}

        @self.app.exception_handler(RequestValidationError)
        async def validation_exception_handler(_request: Request, exc: RequestValidationError):
            errors = [
                {
                    "field": ".".join(map(str, err["loc"][1:])),  # skip 'body'
                    "message": err["msg"]
                }
                for err in exc.errors()
            ]
            return JSONResponse(
                status_code=422,
                content={"errors": errors}
            )

        # include routers
        self.app.include_router(v1_routers, prefix='/api', tags=["v1"])


app_creator = App()
app = app_creator.app
db = app_creator.db
container = app_creator.container
