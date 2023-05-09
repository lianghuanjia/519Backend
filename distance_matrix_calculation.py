import numpy as np
from google_map_distance_matrix_api import calculate_traveling_time_between_two_places, convert_seconds
from TSP_problem_google_solution import get_optimized_route


def calculate_time_between_2_places(lat1, lon1, lat2, lon2, travel_mode):
    p1 = (lat1, lon1)
    p2 = (lat2, lon2)
    traveling_time_in_second = calculate_traveling_time_between_two_places(p1, p2, travel_mode)
    return traveling_time_in_second


def get_data_set(location_list, travel_mode):
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
    # print("===route_list ====")
    # print(route_list)
    result = []
    for i in range(len(route_list) - 1): #i=0,1,2
        current_place_index = route_list[i]
        place_name = location_list[current_place_index][0]
        next_place_index = route_list[i + 1]
        time_to_next_place_in_second = duration_matrix[current_place_index][next_place_index]
        time_to_next_place_str = convert_seconds(time_to_next_place_in_second)
        place_name_and_time_to_next_place = (place_name, time_to_next_place_str)
        result.append(place_name_and_time_to_next_place)
    return result


def get_display_result_for_last_place_to_destination(last_place_info, destination_info, mode):
    # print("==================")
    # print(last_place_info)
    # print(destination_info)
    duration = calculate_time_between_2_places(last_place_info[1], last_place_info[2], destination_info[1],
                                               destination_info[2], mode)
    return last_place_info[0], str(convert_seconds(duration))


def get_locations_and_mode_to_get_display_result(locations, mode):
    # TO DO: Need to check if the locations list is empty
    destination_info = locations[-1]
    all_but_last = locations[:-1]
    print(all_but_last)
    matrix = get_data_set(all_but_last, mode)
    print(matrix)
    route = get_optimized_route(matrix)
    print("Got the route: "+str(route))


    # last place from the optimized route
    last_place_index = route[-1]
    result = extract_information(all_but_last, route, matrix)
    # print(result)
    print(locations[last_place_index])
    print(all_but_last[last_place_index])
    result.append(get_display_result_for_last_place_to_destination(all_but_last[last_place_index], destination_info, mode))
    result.append((destination_info[0], str(0)))
    return result


if __name__ == "__main__":
    starting_point = ('Monmouth Street Park', 42.3453547, -71.1068336)
    # place1 = ('Museum of Fine Arts, Boston', 42.339381, -71.094048)
    place1 = ('Monmouth Street Park', 42.3453547, -71.1068336)
    # place2 = ('Caffè Bene', 42.3423715, -71.0847774)
    # destination = ('Gabel Museum of Archaeology', 42.3501187, -71.1037303)
    destination = ('Monmouth Street Park', 42.3453547, -71.1068336)
    locations = [starting_point, place1, destination]
    mode = "driving"
    result = get_locations_and_mode_to_get_display_result(locations, mode)
    print(result)
# data_model = [[0, 442, 574, 480],
#               [442, 0, 307, 561],
#               [574, 307, 0, 574],
#               [480, 561, 574, 0]]
