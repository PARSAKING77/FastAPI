from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    descreption = Column(String)
    priorty = Column(Integer)
    complite = Column(Boolean, default=False)