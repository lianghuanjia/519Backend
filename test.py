# import ast
#
#
# starting_point = "['Monmouth Street Park', '42.3453547', '-71.1068336']"
# destination = "['Gabel Museum of Archaeology', '42.3501187', '-71.1037303']"
# places = "['Museum of Fine Arts, Boston', '42.339381', '-71.094048', 'Caffè Bene', '42.3423715', '-71.0847774']"
#
# def process_start_and_destination(a_place):
#     try:
#         list_from_string = ast.literal_eval(a_place)
#         processed_place_with_detail = get_all_places_with_their_lant_long(list_from_string)
#         return processed_place_with_detail
#     except Exception as err:
#         print(err)
#
# def get_all_places_with_their_lant_long(list_of_places_info):
#     if len(list_of_places_info) % 3 != 0:
#         raise ValueError("Invalid length of the list of places info")
#     num_of_places = len(list_of_places_info) // 3
#     all_places_and_info = []
#     index = 0
#     for i in range(num_of_places):
#         place_dic = {}
#         place_dic["place_name"] = list_of_places_info[index]
#         index += 1
#         place_dic["latitude"] = list_of_places_info[index]
#         index += 1
#         place_dic["longitude"] = list_of_places_info[index]
#         index += 1
#         all_places_and_info.append(place_dic)
#     return all_places_and_info
#
#
# def process_places(all_places):
#     list_of_all_places = ast.literal_eval(all_places)
#     categorized_places_list = get_all_places_with_their_lant_long(list_of_all_places)
#     return categorized_places_list
#
#
# if __name__ == "__main__":
    # processed_starting_point = process_start_and_destination(starting_point)
    # processed_destination_point = process_start_and_destination(destination)
    # processed_places = process_places(places)
    # print(processed_starting_point)
    # print(processed_destination_point)
    # print(processed_places)
    # for i in processed_places:
    #     print(i["place_name"])
    #     print(i["latitude"])
    #     print(i["longitude"])
    # get_a_place_details(places)
    # a = '42.3453547'
    # b = '-71.1068336'
    # print(float(b))
#
#
#
#
