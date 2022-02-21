from lib2to3.pytree import Base
from sqlalchemy import Column, Integer, String

class Repo(Base):
    __tablename__ = 'repos'
    