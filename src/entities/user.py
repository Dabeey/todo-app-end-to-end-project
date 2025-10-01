from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database.core import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(email={self.email}, last_name={self.first_name}, first_name={self.last_name} )>"
    