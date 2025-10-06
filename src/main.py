from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .rate_limiter import limiter
from .database.core import engine, Base
from .entities.todo import Todo  # Import models to register them
from .entities.user import User
from .api import register_routes
from .logger_config import configure_logging, LogLevels

configure_logging(LogLevels.INFO)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

"""
Only uncomment below to create new tables when a database is available.
Leaving this enabled without a DB connection will crash startup.
"""
try:
    Base.metadata.create_all(bind=engine)
except Exception:
    # Avoid startup crash in environments without DB connection
    pass

register_routes(app)