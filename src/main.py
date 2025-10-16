from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .rate_limiter import limiter
from .database.core import engine, Base
from .entities.todo import Todo  # Import models to register them
from .entities.user import User
from .api import register_routes
from .logger_config import configure_logging, LogLevels
from fastapi.openapi.utils import get_openapi


configure_logging(LogLevels.INFO)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


try:
    Base.metadata.create_all(bind=engine)
except Exception:
    # Avoid startup crash in environments without DB connection
    pass

register_routes(app)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Modern Todo App",
        version="1.0.0",
        description="An Ultra modern Productivity App built with FastAPI, PostgreSQL, and React.",
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    # Add global security
    openapi_schema["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

