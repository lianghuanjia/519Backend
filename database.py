import traceback
from database_connection_configuration import username, password, endpoint, port, database_name
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()

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
        traceback.print_exc()
        print(e)



def create_session():
    engine = create_db_connection()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def get_session():
    db_session = create_session()
    return db_session

