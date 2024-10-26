from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed = Column(String)
    is_ative = Column(Boolean, default=True)
    role = Column(String)




class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    descreption = Column(String)
    priorty = Column(Integer)
    complite = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))