from fastapi import FastAPI
from .database.core import engine, Base
from .entities.todo import Todo # Import models to register them
from .entities.user import User
from .api import register_routes
from .logging import configure_logging, LogLevels

configure_logging(LogLevels.info)

app = FastAPI()

"""
Only unvomment below to create new tables, 
otherwise the test will fail if not connected
"""
Base.metadata.create_all(bind=engine)

register_routes(app)