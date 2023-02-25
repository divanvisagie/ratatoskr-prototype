from sqlalchemy import DateTime, ForeignKey, create_engine, Column, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_username = Column(String)
    insert_time = Column(String)


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    question = Column(String)
    answer = Column(String)
    filter_name = Column(String)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="history")

User.history = relationship("History", order_by=History.id, back_populates="user")