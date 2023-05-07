from itinerary import *


def test_check_correct_start_location_format():
    correct_start_location = "['Your Location', '42.3455898', '-71.0887769']"
    assert check_one_place_format(correct_start_location) == True

def test_check_incorrect_start_location_format():
    empty_start_location = "['', '42.3455898', '-71.0887769']"
    empty_latitude = "['Your Location', '', '-71.0887769']"
    empty_longitude = "['Your Location', '42.3455898', '']"
    invalid_latitude = "['Your Location', 'not a latitude', '-71.0887769']"
    invalid_longitude = "['Your Location', '42.3455898', 'invalid longitude']"
    list_of_2_info = "['42.3455898', '-71.0887769']"
    assert check_one_place_format(empty_start_location) == False
    assert check_one_place_format(empty_latitude) == False
    assert check_one_place_format(empty_longitude) == False
    assert check_one_place_format(invalid_latitude) == False
    assert check_one_place_format(invalid_longitude) == False
    assert check_one_place_format(list_of_2_info) == False

def test_check_correct_places():
    places_str = "['Museum of Fine Arts, Boston', '42.339381', '-71.094048', 'Caffè Bene', '42.3423715', '-71.0847774']"
    assert check_places_format(places_str) == True
    one_place_str = "['Museum of Fine Arts, Boston', '42.339381', '-71.094048']"
    assert check_places_format(one_place_str) == True
    three_places_str = "['Museum of Fine Arts, Boston', '42.339381', '-71.094048', 'Caffè Bene', '42.3423715', '-71.0847774', 'Monmouth Street Park', '42.3453547', '-71.1068336']"
    assert check_places_format(three_places_str) == True

def test_check_incorrect_places():
    not_multiplication_of_three_places_list = "[ '42.339381', '-71.094048', 'Caffè Bene', '42.3423715', '-71.0847774']"
    assert check_places_format(not_multiplication_of_three_places_list) == False
    invalid_latitude_places_list = "['Museum of Fine Arts, Boston', 'invalid_latitude', '-71.094048', 'Caffè Bene', '42.3423715', '-71.0847774']"
    assert check_places_format(invalid_latitude_places_list) == False
    invalid_longitude_places_list = "['Museum of Fine Arts, Boston', '42.339381', 'invalid longitude', 'Caffè Bene', '42.3423715', '-71.0847774']"
    assert check_places_format(invalid_longitude_places_list) == False



