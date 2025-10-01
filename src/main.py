from fastapi import FastAPI
from .database.core import engine, Base
from .entities.todo import Todo # Import models to register them
from .entities.user import User
from .api import register_routes


app = FastAPI()

"""
Only unvomment below to create new tables, 
otherwise the test will fail if not connected
"""

register_routes(app)