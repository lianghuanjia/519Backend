from database import get_session
from database_table_definition import User, Itinerary
from datetime import datetime
from itinerary import process_starting_point_and_destination, process_places
from distance_matrix_calculation import get_locations_and_mode_to_get_display_result

import ast


def user_exists(target_email):
    """
    Use it to check if a user exists in the database by checking the if user's email in the database
    :param target_email:
    :return:
    """
    db_session = get_session()
    user_exists_result = db_session.query(User).filter_by(email=target_email).first() is not None
    return user_exists_result


def delete_user_in_database(user_email):
    """
    Use it to delete a user in the database
    :param user_email:
    :return:
    """
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
    """
    Use it to delete an itinerary in the database
    :param itinerary_id:
    :return:
    """
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
    """
    Use it to get current datetime in DATETIME format
    :return:
    """
    now = datetime.now()
    # Format the datetime object as a string in the correct format for a SQL DATETIME column
    sql_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
    return sql_datetime


def get_a_user_itineraries_from_database(user_email):
    """
    Use it to get a user's all itineraries from database
    :param user_email:
    :return:
    """
    try:
        db_session = get_session()
        rows = db_session.query(Itinerary).filter(Itinerary.user_email == user_email).all()
        return rows
    except Exception as err:
        print(err)


def get_an_itinerary_from_database(itinerary_id):
    """
    Use it to get a specific itinerary by looking up the itinerary_id
    :param itinerary_id:
    :return:
    """
    try:
        db_session = get_session()
        itinerary = db_session.query(Itinerary).filter_by(id=itinerary_id).first()
        return itinerary
    except Exception as err:
        print(err)


def process_a_user_all_itineraries_response(all_itineraries):
    """
    Use it to decorate a user's all itineraries and return the information that is suitable
    to be displayed in the phone
    :param all_itineraries:
    :return:
    """
    try:
        if all_itineraries is None or len(all_itineraries) == 0:
            return []
        else:
            response = []
            for each_itinerary in all_itineraries:
                each_itinerary_container = {}
                # print(each_itinerary.starting_point)
                # print(each_itinerary.destination)
                starting_point = ast.literal_eval(each_itinerary.starting_point)[0]
                destination = ast.literal_eval(each_itinerary.destination)[0]
                # print(starting_point)
                # print(destination)
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
    """
    Use it to get optimized route
    :param travel_mode:
    :param db_itinerary:
    :return:
    """
    starting_point_info = process_starting_point_and_destination(db_itinerary.starting_point)[0]
    destination_info = process_starting_point_and_destination(db_itinerary.destination)[0]
    places_info_list = process_places(db_itinerary.places)
    """
    how it looks like:
    {'place_name': 'Your Location', 'latitude': '42.3455898', 'longitude': '-71.0887769'}
    {'place_name': 'Boston Public Library - Central Library', 'latitude': '42.3493136', 'longitude': '-71.0781875'}
    [{'place_name': 'Park', 'latitude': '42.3465259', 'longitude': '-71.0822474'}, {'place_name': 'Cafe 939', 'latitude': '42.3481677', 'longitude': '-71.0849947'}]

    make it like this:
    
    starting_point = ('Monmouth Street Park', 42.3453547, -71.1068336)
    place1 = ('Museum of Fine Arts, Boston', 42.339381, -71.094048)
    place2 = ('Caffè Bene', 42.3423715, -71.0847774)
    destination = ('Gabel Museum of Archaeology', 42.3501187, -71.1037303)
    """
    starting_point = (
    starting_point_info['place_name'], float(starting_point_info['latitude']), float(starting_point_info['longitude']))
    location_list = [starting_point]

    for each_place in places_info_list:
        location_list.append((each_place['place_name'], float(each_place['latitude']), float(each_place['longitude'])))

    destination_point = (
    destination_info['place_name'], float(destination_info['latitude']), float(destination_info['longitude']))
    location_list.append(destination_point)
    # print("===location list====")
    # print(location_list)
    # Finish organizing the locations so that they are ready to be
    # processed in the helper function to get optimized routes
    display_info = get_locations_and_mode_to_get_display_result(location_list, travel_mode)
    return display_info


# if __name__ == "__main__":
#     starting_point = ('Boston Public Library - Central Library', 42.3493136, -71.0781875)
#     # place1 = ('Museum of Fine Arts, Boston', 42.339381, -71.094048)
#     place2 = ('Boston Public Library - Central Library', 42.3493136, -71.0781875)
#     destination = ('Boston Public Library - Central Library', 42.3493136, -71.0781875)
#     loc_list = [starting_point, place2, destination]
#     mode = "transit"
#     display_info = get_locations_and_mode_to_get_display_result(loc_list, mode)
#     print(display_info)
