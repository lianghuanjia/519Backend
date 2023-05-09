from google_map_distance_matrix_api import calculate_traveling_time_between_two_places

"""
Use this module to write tests that are related to Google Map Distance Matrix API 
"""


def test_same_location_duration():
    p1 = (40.714, -73.998)
    p2 = (40.714, -73.998)
    mode = "driving"
    assert calculate_traveling_time_between_two_places(p1, p2, mode) == 0
