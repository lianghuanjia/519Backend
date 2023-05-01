import traceback

from sqlalchemy import create_engine, Column, String, Integer, DATETIME, TIME, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

endpoint = 'database-1.cv70rzejhsog.us-east-1.rds.amazonaws.com'
username = 'admin'
password = '519android'
database_name = 'MobileClassFinalProject'
port = "3306"
Base = declarative_base()

app = FastAPI()


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


def create_db_connection():
    try:
        db_engine = create_engine(
            "mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}".format(username=username,
                                                                                  password=password,
                                                                                  host=endpoint,
                                                                                  port=port,
                                                                                  dbname=database_name))
        return db_engine
    except Exception as e:
        print(e)


engine = create_db_connection()


class AddUserItem(BaseModel):
    email: str
    username: str
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    tripPreference: Optional[str] = None

class AddItineraryItem(BaseModel):
    user_email: str
    starting_point: str
    destination: str
    places: Optional[str] = None


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


@app.post("/add-user/")
def add_user_to_database(item: AddUserItem):
    try:
        if item.email == "":
            return JSONResponse(status_code=400, content={'message':'Missing user email'})
        if item.username == "":
            return JSONResponse(status_code=400, content={'message': 'Missing username'})
        if user_exists(item.email):
            return JSONResponse(status_code=400, content={'message': 'User exists already'})
        new_user = User(email=item.email, username=item.username, phone=item.phone, age=item.age, gender=item.gender,
                        tripPreference=item.tripPreference)
        db_session = get_session()
        db_session.add(new_user)
        db_session.commit()
        return JSONResponse(status_code=200, content={'message': 'Add user successfully'})
    except Exception as e:
        traceback.print_exc()
        delete_user_in_database(item.email)
        raise HTTPException(status_code=500, detail='Internal Error')


@app.post("/add-itinerary/")
def add_itinerary_to_database(item: AddItineraryItem):
    try:
        if item.user_email == "":
            return JSONResponse(status_code=400, content={'message': 'Missing user email'})
        if item.starting_point == "":
            return JSONResponse(status_code=400, content={'message': 'Missing starting point'})
        if item.destination == "":
            return JSONResponse(status_code=400, content={'message': 'Missing destination'})
        if not user_exists(item.user_email):
            return JSONResponse(status_code=400, content={'message': 'No such user in database'})
        new_itinerary = Itinerary(user_email=item.user_email,starting_point=item.starting_point,destination=item.destination,places=item.places)
        db_session = get_session()
        db_session.add(new_itinerary)
        db_session.commit()
        return JSONResponse(status_code=200, content={'message': 'Add itinerary successfully'})
    except Exception as e:
        traceback.print_exc()
        delete_user_in_database(item.user_email)
        raise HTTPException(status_code=500, detail='Internal Error')


def user_exists(target_email):
    db_session = get_session()
    user_exists_result = db_session.query(User).filter_by(email=target_email).first() is not None
    return user_exists_result


def delete_user_in_database(user_email):
    try:
        db_session = get_session()
        row = db_session.query(User).filter_by(email=user_email).one_or_none()
        if row is not None:
            db_session.delete(row)
            db_session.commit()
        db_session.close()
    except Exception as e:
        print(e)
        raise Exception()
