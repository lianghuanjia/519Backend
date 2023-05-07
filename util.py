from database import get_session
from database_table_definition import User

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