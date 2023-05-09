import numpy as np
from google_map_distance_matrix_api import calculate_traveling_time_between_two_places, convert_seconds
from TSP_problem_google_solution import get_optimized_route
from google_direction_api import get_direction_from_one_place_to_another

"""
Use this file to get the optimized route in an itinerary
"""


def calculate_time_between_2_places(lat1, lon1, lat2, lon2, travel_mode):
    """
    Use it to calculate the time taken to travel between one place to another
    :param lat1: latitude of the first place
    :param lon1: longitude of the second place
    :param lat2: latitude of the first place
    :param lon2: longitude of the second place
    :param travel_mode: The travel mode that the user prefers
    :return: the travel time from place 1 to place 2 in SECOND UNIT
    """
    p1 = (lat1, lon1)
    p2 = (lat2, lon2)
    traveling_time_in_second = calculate_traveling_time_between_two_places(p1, p2, travel_mode)
    return traveling_time_in_second


def get_data_set(location_list, travel_mode):
    """
    Use this function to generate a distance matrix so that we can use it in the Google TSP solution to calculate the optimized route
    :param location_list: The list that contains all the places. It needs to follow: [starting_point, place1, ... place n, destination]
    e.g.: The location_list looks like this:
    [('Monmouth Street Park', 42.3453547, -71.1068336),('Museum of Fine Arts, Boston', 42.339381, -71.094048), ('Caffè Bene', 42.3423715, -71.0847774),('Gabel Museum of Archaeology', 42.3501187, -71.1037303)]
    :param travel_mode: the travel mode the user prefers
    :return: a distance matrix that each data is int inside
    """
    n = len(location_list)
    dist_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(i + 1, n):
            dist = calculate_time_between_2_places(location_list[i][1], location_list[i][2], location_list[j][1],
                                                   location_list[j][2],
                                                   travel_mode)
            dist_matrix[i][j] = dist
            dist_matrix[j][i] = dist

    converted_matrix = dist_matrix.astype(int)
    return converted_matrix


def extract_information(location_list, route_list, duration_matrix):
    """
    Use this function to convert the optimized route returned by Google TSP solution to match our places' name, and get
    the traveling time between places based on the optimized route
    :param location_list: The location list of the itinerary
    :param route_list: The optimized route Google TSP solution gives us
    :param duration_matrix: The distance matrix we calculate. It contains the travel time between all the places.
    :return: return a list that contains multiple sub_list, with each sub_list containing the place's name and the time
    it takes to go to the next place based on the optimized route
    """
    result = []
    for i in range(len(route_list) - 1):  # i=0,1,2
        current_place_index = route_list[i]
        place_name = location_list[current_place_index][0]
        next_place_index = route_list[i + 1]
        time_to_next_place_in_second = duration_matrix[current_place_index][next_place_index]
        time_to_next_place_str = convert_seconds(time_to_next_place_in_second)
        place_name_and_time_to_next_place = (place_name, time_to_next_place_str)
        result.append(place_name_and_time_to_next_place)
    return result


def get_display_result_for_last_place_to_destination(last_place_info, destination_info, mode):
    """
    Use it to get display result for the last place on the Google optimized route to the destination.
    We have this method because when we calculate the optimized route, we exclude the destination, because I haven't
    figured out how to run a TSP solution with the destination not the same as the starting point.
    :param last_place_info: The last place in the optimized route
    :param destination_info: The destination in the itinerary
    :param mode: The travel mode the user prefers
    :return: a tuple contains the last place in the optimized route, and its traveling time to the destination
    """
    duration = calculate_time_between_2_places(last_place_info[1], last_place_info[2], destination_info[1],
                                               destination_info[2], mode)
    return last_place_info[0], str(convert_seconds(duration))


def get_directions_for_display(optimized_route, destination_info, location_info_list, travel_mode):
    # First get the directions for the places in the optimized route
    directions_results_for_whole_itinerary = []
    for i in range(len(optimized_route) - 1):
        place_index = optimized_route[i]
        starting_place = location_info_list[place_index]
        end_place_index = optimized_route[i + 1]
        end_place = location_info_list[end_place_index]
        starting_place_lat_and_long = str(starting_place[1]) + ", " + str(starting_place[2])
        end_place_lat_and_long = str(end_place[1]) + ", " + str(end_place[2])
        direction = get_direction_from_one_place_to_another(starting_place_lat_and_long, end_place_lat_and_long,
                                                            travel_mode)
        directions_results_for_whole_itinerary.append(direction)

    # Then add the last place in the optimized route's direction to the destination_info
    last_place_in_route_index = optimized_route[-1]
    last_place_in_route_lat_long = str(location_info_list[last_place_in_route_index][1]) + ", " + str(
        location_info_list[last_place_in_route_index][2])
    destination_lat_long = str(destination_info[1]) + ", " + str(destination_info[2])
    # print("+=========")
    # print(last_place_in_route_lat_long)
    # print(destination_lat_long)
    # print("+=========")
    directions_results_for_whole_itinerary.append(get_direction_from_one_place_to_another(last_place_in_route_lat_long, destination_lat_long, travel_mode))
    return directions_results_for_whole_itinerary

def get_locations_and_mode_to_get_display_result(locations, mode):
    # TO DO: Need to check if the locations list is empty: No need to check.
    destination_info = locations[-1]
    all_but_last = locations[:-1]
    # print(all_but_last)
    matrix = get_data_set(all_but_last, mode)
    # print(matrix)
    route = get_optimized_route(matrix)
    # print("Got the route: " + str(route))
    # GET THE DIRECTIONS FOR THE ROUTE AND WITH THE DESTINATION INSIDE:
    directions_list = get_directions_for_display(route, destination_info, locations, mode)
    # last place from the optimized route
    last_place_index = route[-1]
    place_and_duration = extract_information(all_but_last, route, matrix)
    # print(result)
    # print(locations[last_place_index])
    # print(all_but_last[last_place_index])
    place_and_duration.append(
        get_display_result_for_last_place_to_destination(all_but_last[last_place_index], destination_info, mode))
    place_and_duration.append((destination_info[0], str(0)))
    return place_and_duration, directions_list


# if __name__ == "__main__":
#     starting_point = ('Monmouth Street Park', 42.3453547, -71.1068336)
#     # place1 = ('Museum of Fine Arts, Boston', 42.339381, -71.094048)
#     place1 = ('Monmouth Street Park', 42.3453547, -71.1068336)
#     # place2 = ('Caffè Bene', 42.3423715, -71.0847774)
#     # destination = ('Gabel Museum of Archaeology', 42.3501187, -71.1037303)
#     destination = ('Monmouth Street Park', 42.3453547, -71.1068336)
#     locations = [starting_point, place1, destination]
#     mode = "driving"
#     result = get_locations_and_mode_to_get_display_result(locations, mode)
#     print(result)
# data_model = [[0, 442, 574, 480],
#               [442, 0, 307, 561],
#               [574, 307, 0, 574],
#               [480, 561, 574, 0]]
