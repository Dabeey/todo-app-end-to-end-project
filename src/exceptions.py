from fastapi import HTTPException

class TodoError(HTTPException):
    """Base exception for todo-related errors"""
    pass
class TodoNotFoundError(TodoError):
    def __init__(self, todo_id = None):
        message = 'Todo not found' if todo_id is None else f'Todo with id {todo_id} not found'
        super().__init__(status_code=404, detail=message)


class TodoCreationError(TodoError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f'Failed to create todo: {error}')


