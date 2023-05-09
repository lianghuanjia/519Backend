import ast
from datetime import datetime


def process_starting_point_and_destination(a_place):
    """
    Use it to convert a list that is in string format into a dictionary that contains all the list's information
    :param a_place: A list in string format that contains a place's information, it looks like this:  "['Monmouth Street Park', '42.3453547', '-71.1068336']"
    :return: A list that contains a dictionary that looks like this: {'place_name': 'Monmouth Street Park', 'latitude': '42.3453547', 'longitude': '-71.1068336'}
    """
    try:
        list_from_string = ast.literal_eval(a_place)
        processed_place_with_detail = get_all_places_with_their_lant_long(list_from_string)
        return processed_place_with_detail
    except Exception as err:
        print(err)


def process_places(all_places):
    """
    Use this function to process all_places list in string format to a list that contains dictionary(s) that each dictionary represents a place's information
    :param all_places: "['Museum of Fine Arts, Boston', '42.339381', '-71.094048', 'Caffè Bene', '42.3423715', '-71.0847774']"
    :return: [{'place_name': 'Museum of Fine Arts, Boston', 'latitude': '42.339381', 'longitude': '-71.094048'}, {'place_name': 'Caffè Bene', 'latitude': '42.3423715', 'longitude': '-71.0847774'}]
    """
    list_of_all_places = ast.literal_eval(all_places)
    categorized_places_list = get_all_places_with_their_lant_long(list_of_all_places)
    return categorized_places_list


def get_all_places_with_their_lant_long(list_of_places_info):
    """
    Use it extract all the places from the list in string format that contains all the places' information
    :param list_of_places_info: "['Museum of Fine Arts, Boston', '42.339381', '-71.094048', 'Caffè Bene', '42.3423715', '-71.0847774']"
    :return: a list of dictionary, with each dictionary contains a place's name, its latitude, and its longitude.
        It looks like this:
            [{'place_name': 'Park', 'latitude': '42.3465259', 'longitude': '-71.0822474'}, {'place_name': 'Cafe 939', 'latitude': '42.3481677', 'longitude': '-71.0849947'}]
    """
    list_of_places_info_len = len(list_of_places_info)
    if list_of_places_info_len % 3 != 0:
        raise ValueError("Invalid length of the list of places info")
    num_of_places = len(list_of_places_info) // 3
    all_places_and_info = []
    index = 0
    for i in range(num_of_places):
        place_dic = {}
        place_dic["place_name"] = list_of_places_info[index]
        index += 1
        place_dic["latitude"] = list_of_places_info[index]
        index += 1
        place_dic["longitude"] = list_of_places_info[index]
        index += 1
        all_places_and_info.append(place_dic)
    return all_places_and_info


def check_one_place_format(location_input):
    """
    Use it to check if a location in the request body meets the requirement, i.e.: In a string format, in a list,
    contains only 3 things: place name, latitude, longitude
    :param location_input: "['Monmouth Street Park', '42.3453547', '-71.1068336']"
    :return: True if it meets the requirement, False otherwise
    """
    try:
        location_in_list_format = ast.literal_eval(location_input)
        if len(location_in_list_format) != 3:
            return False
        if location_in_list_format[0] == "" or location_in_list_format is None:
            return False
        float(location_in_list_format[1])
        float(location_in_list_format[2])
        return True

    except Exception as err:
        print(err)
        return False


def check_places_format(places_input):
    """
    Use it to check if the places input format from the add-itinerary endpoint meets the requirements
    :param places_input: "['Museum of Fine Arts, Boston', '42.339381', '-71.094048', 'Caffè Bene', '42.3423715', '-71.0847774']"
    :return: True if the places input meets the requirement. False otherwise.
    """
    try:
        places_in_list_format = ast.literal_eval(places_input)
        if len(places_in_list_format) % 3 != 0:
            return False
        num_of_places = len(places_in_list_format) // 3
        index = 0
        for i in range(num_of_places):
            one_place_list = []
            one_place_list.append(places_in_list_format[index])
            index += 1
            one_place_list.append(places_in_list_format[index])
            index += 1
            one_place_list.append(places_in_list_format[index])
            index += 1
            if not check_one_place_format(str(one_place_list)):
                return False
        return True
    except Exception as err:
        print(err)
        return False


def check_datetime(datetime_input):
    """
    Use it to check the datetime from the add-itinerary request body is in datetime format and it can be put in the
    MySQL database as DATETIME format
    :param datetime_input:
    :return: True if the datetime_input is a datetime.
    """
    return isinstance(datetime_input, datetime)


