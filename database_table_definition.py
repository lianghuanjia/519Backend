from sqlalchemy import Column, String, Integer, DATETIME, ForeignKey
from sqlalchemy.orm import declarative_base


Base = declarative_base()



class User(Base):
    __tablename__ = "user"

    email = Column(String(50), primary_key=True)
    username = Column(String(45))
    phone = Column(String(45), nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(45), nullable=True)
    tripPreference = Column(String(45), nullable=True)


class Itinerary(Base):
    __tablename__ = "itinerary"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_email = Column(String(50), ForeignKey("user.email"))
    starting_point = Column(String(45))
    destination = Column(String(45))
    places = Column(String(45), nullable=True)
    itinerary_name = Column(String(45), nullable=True)
    created_time = Column(DATETIME, nullable=True)

