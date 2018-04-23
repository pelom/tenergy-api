from env import datetime_now_tz

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(30), nullable=False)
    LastName = Column(String(120), nullable=False)
    Username = Column(String(120), unique=True)
    Password = Column(String(255), nullable=False)
    Email = Column(String(120), nullable=False)

    CreatedDate = Column(DateTime(timezone=True), default=datetime_now_tz)