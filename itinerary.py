import ast
from datetime import datetime
from database import get_session
from database_table_definition import Itinerary

starting_point = "['Monmouth Street Park', '42.3453547', '-71.1068336']"
destination = "['Gabel Museum of Archaeology', '42.3501187', '-71.1037303']"
places = "['Museum of Fine Arts, Boston', '42.339381', '-71.094048', 'Caffè Bene', '42.3423715', '-71.0847774']"

def process_starting_point_and_destination(a_place):
    try:
        list_from_string = ast.literal_eval(a_place)
        processed_place_with_detail = get_all_places_with_their_lant_long(list_from_string)
        return processed_place_with_detail
    except Exception as err:
        print(err)

def process_places(all_places):
    list_of_all_places = ast.literal_eval(all_places)
    categorized_places_list = get_all_places_with_their_lant_long(list_of_all_places)
    return categorized_places_list


def get_all_places_with_their_lant_long(list_of_places_info):
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
    try:
        places_in_list_format = ast.literal_eval(places_input)
        if len(places_in_list_format) % 3 != 0:
            return False
        num_of_places = len(places_in_list_format) // 3
        index = 0
        for i in range(num_of_places):
            one_place_list = []
            one_place_list.append(places_in_list_format[index])
            index+=1
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
    return isinstance(datetime_input, datetime)




# if __name__ == "__main__":
    # processed_starting_point = process_add_itinerary_start_and_destination(starting_point)
    # processed_destination_point = process_add_itinerary_start_and_destination(destination)
    # processed_places = process_add_itinerary_places(places)
    # print(processed_starting_point)
    # print(processed_destination_point)
    # print(processed_places)
    # for i in processed_places:
    #     print(i["place_name"])
    #     print(i["latitude"])
    #     print(i["longitude"])
    # get_a_place_details(places)
    # places_str = "['Museum of Fine Arts, Boston', '42.339381', '-71.094048', 'Caffè Bene', '42.3423715', '-71.0847774']"
    # check_places_format(places_str)




