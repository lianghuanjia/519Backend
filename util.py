from database import get_session
from database_table_definition import User, Itinerary
from datetime import datetime
from itinerary import process_starting_point_and_destination, process_places

import ast
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

def delete_itinerary_in_database(itinerary_id):
    try:
        db_session = get_session()
        row = db_session.query(Itinerary).filter_by(id=itinerary_id).one_or_none()
        if row is not None:
            db_session.delete(row)
            db_session.commit()
        db_session.close()
    except Exception as err:
        print(err)

def get_current_datetime_in_SQL_DATETIME_format():
    now = datetime.now()
    # Format the datetime object as a string in the correct format for a SQL DATETIME column
    sql_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
    return sql_datetime


def get_a_user_itineraries_from_database(user_email):
    try:
        db_session = get_session()
        rows = db_session.query(Itinerary).filter(Itinerary.user_email==user_email).all()
        return rows
    except Exception as err:
        print(err)

def get_an_itinerary_from_database(itinerary_id):
    try:
        db_session = get_session()
        itinerary = db_session.query(Itinerary).filter_by(id=itinerary_id).first()
        return itinerary
    except Exception as err:
        print(err)

def process_a_user_all_itineraries_response(all_itineraries):
    try:
        if all_itineraries is None or len(all_itineraries) == 0:
            return []
        else:
            response = []
            for each_itinerary in all_itineraries:
                each_itinerary_container = {}
                print(each_itinerary.starting_point)
                print(each_itinerary.destination)
                starting_point = ast.literal_eval(each_itinerary.starting_point)[0]
                destination = ast.literal_eval(each_itinerary.destination)[0]
                print(starting_point)
                print(destination)
                itinerary_name = "FROM [{start}] TO [{end}]".format(start=starting_point, end=destination)
                each_itinerary_container["itinerary name"] = itinerary_name
                created_time = str(each_itinerary.created_time)
                each_itinerary_container["created time"] = created_time
                each_itinerary_container["id"] = str(each_itinerary.id)
                response.append(each_itinerary_container)
            return response
    except Exception as err:
        print(err)
        raise err



def get_optimized_order(travel_mode, db_itinerary):
    starting_point_info = process_starting_point_and_destination(db_itinerary.starting_point)[0]
    destination_info = process_starting_point_and_destination(db_itinerary.destination)[0]
    places_info_list = process_places(db_itinerary.places)
    # optimized_route =

