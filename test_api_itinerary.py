import traceback
from util import delete_itinerary_in_database, get_current_datetime_in_SQL_DATETIME_format
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException
from api_application import app
import API_path_values
import json

client = TestClient(app)

# class AddItineraryItem(BaseModel):
#     user_email: str
#     starting_point: str
#     destination: str
#     places: Optional[str] = None
#     itinerary_name: Optional[str] = None
#     created_time: Optional[datetime] = None


CORRECT_ADD_ITINERARY_INPUT = {
                        "user_email":"new_user@bu.edu",
                      "starting_point":"['Your Location', '42.3455898', '-71.0887769']",
                      "destination":"['Boston Public Library - Central Library', '42.3493136', '-71.0781875']",
                      "places":"['Park', '42.3465259', '-71.0822474', 'Cafe 939', '42.3481677', '-71.0849947']"}

# data = {
#     "user_email": "new_user@bu.edu",
#     "starting_point": "['Your Location', '42.3455898', '-71.0887769']",
#     "destination": "['Boston Public Library - Central Library', '42.3493136', '-71.0781875']",
#     "places": "['Park', '42.3465259', '-71.0822474', 'Cafe 939', '42.3481677', '-71.0849947']"
# }

def test_add_itinerary_with_correct_json_input():
    try:
        add_itinerary_response = client.post(API_path_values.ADD_ITINERARY_PATH, json=CORRECT_ADD_ITINERARY_INPUT)
        assert add_itinerary_response.status_code == 200
        decoded_response = json.loads(add_itinerary_response.content.decode('utf-8'))
        # print(decoded_response['message'])
        assert decoded_response['status code'] == 200
        assert decoded_response['message'] == "Added itinerary successfully"
        itinerary_id = decoded_response['itinerary_id']
        assert isinstance(itinerary_id, int)
        delete_itinerary_in_database(itinerary_id)
    except Exception as err:
        traceback.print_exc()
        assert False

def test_add_itinerary_correct_with_itinerary_name():
    try:
        CORRECT_ADD_ITINERARY_JSON = CORRECT_ADD_ITINERARY_INPUT
        CORRECT_ADD_ITINERARY_JSON["itinerary_name"] = "My favorite itinerary"
        add_itinerary_response = client.post(API_path_values.ADD_ITINERARY_PATH, json=CORRECT_ADD_ITINERARY_JSON)
        assert add_itinerary_response.status_code == 200
        decoded_response = json.loads(add_itinerary_response.content.decode('utf-8'))
        # print(decoded_response['message'])
        assert decoded_response['status code'] == 200
        assert decoded_response['message'] == "Added itinerary successfully"
        itinerary_id = decoded_response['itinerary_id']
        assert isinstance(itinerary_id, int)
        delete_itinerary_in_database(itinerary_id)
    except Exception as err:
        traceback.print_exc()
        assert False

def test_add_itinerary_correct_with_created_time():
    try:
        CORRECT_ADD_ITINERARY_JSON = CORRECT_ADD_ITINERARY_INPUT
        CORRECT_ADD_ITINERARY_JSON["created_time"] = get_current_datetime_in_SQL_DATETIME_format()
        add_itinerary_response = client.post(API_path_values.ADD_ITINERARY_PATH, json=CORRECT_ADD_ITINERARY_JSON)
        assert add_itinerary_response.status_code == 200
        decoded_response = json.loads(add_itinerary_response.content.decode('utf-8'))
        # print(decoded_response['message'])
        assert decoded_response['status code'] == 200
        assert decoded_response['message'] == "Added itinerary successfully"
        itinerary_id = decoded_response['itinerary_id']
        assert isinstance(itinerary_id, int)
        delete_itinerary_in_database(itinerary_id)
    except Exception as err:
        traceback.print_exc()
        assert False

def test_add_itinerary_correct_with_all_optional_fields():
    try:
        CORRECT_ADD_ITINERARY_JSON = CORRECT_ADD_ITINERARY_INPUT
        CORRECT_ADD_ITINERARY_JSON["itinerary_name"] = "My favorite itinerary"
        CORRECT_ADD_ITINERARY_JSON["created_time"] = get_current_datetime_in_SQL_DATETIME_format()
        add_itinerary_response = client.post(API_path_values.ADD_ITINERARY_PATH, json=CORRECT_ADD_ITINERARY_JSON)
        assert add_itinerary_response.status_code == 200
        decoded_response = json.loads(add_itinerary_response.content.decode('utf-8'))
        # print(decoded_response['message'])
        assert decoded_response['status code'] == 200
        assert decoded_response['message'] == "Added itinerary successfully"
        itinerary_id = decoded_response['itinerary_id']
        assert isinstance(itinerary_id, int)
        delete_itinerary_in_database(itinerary_id)
    except Exception as err:
        traceback.print_exc()
        assert False


def test_add_itinerary_empty_email():
    data = {
        "user_email":"",
        "starting_point":"['Your Location', '42.3455898', '-71.0887769']",
        "destination":"['Boston Public Library - Central Library', '42.3493136', '-71.0781875']",
        "places":"['Park', '42.3465259', '-71.0822474', 'Cafe 939', '42.3481677', '-71.0849947']"
        }
    try:
        add_itinerary_response = client.post(API_path_values.ADD_ITINERARY_PATH, json=data)
        assert add_itinerary_response.status_code == 400
        decoded_response = json.loads(add_itinerary_response.content.decode('utf-8'))
        # print(decoded_response['message'])
        assert decoded_response['status code'] == 400
        assert decoded_response['message'] == "Missing field: user email"
    except Exception as err:
        traceback.print_exc()
        assert False

def test_add_itinerary_invalid_starting_point_with_invalid_latitude():
    data = {
        "user_email": "new_user@bu.edu",
        "starting_point": "['Your Location', 'invalid latitude', '-71.0887769']",
        "destination": "['Boston Public Library - Central Library', '42.3493136', '-71.0781875']",
        "places": "['Park', '42.3465259', '-71.0822474', 'Cafe 939', '42.3481677', '-71.0849947']"
    }
    try:
        add_itinerary_response = client.post(API_path_values.ADD_ITINERARY_PATH, json=data)
        assert add_itinerary_response.status_code == 400
        decoded_response = json.loads(add_itinerary_response.content.decode('utf-8'))
        # print(decoded_response['message'])
        assert decoded_response['status code'] == 400
        assert decoded_response['message'] == "Invalid starting point format. It should be: ['PLACE NAME', 'LATITUDE', 'LONGITUDE']"
    except Exception as err:
        traceback.print_exc()
        assert False

def test_add_itinerary_invalid_destination():
    data = {
        "user_email": "new_user@bu.edu",
        "starting_point": "['Your Location', '42.3455898', '-71.0887769']",
        "destination": "[ '42.3493136', '-71.0781875']",
        "places": "['Park', '42.3465259', '-71.0822474', 'Cafe 939', '42.3481677', '-71.0849947']"
    }
    try:
        add_itinerary_response = client.post(API_path_values.ADD_ITINERARY_PATH, json=data)
        assert add_itinerary_response.status_code == 400
        decoded_response = json.loads(add_itinerary_response.content.decode('utf-8'))
        # print(decoded_response['message'])
        assert decoded_response['status code'] == 400
        assert decoded_response[
                   'message'] == "Invalid destination format. It should be: ['PLACE NAME', 'LATITUDE', 'LONGITUDE']"
    except Exception as err:
        traceback.print_exc()
        assert False

def test_add_itinerary_invalid_places():
    data = {
        "user_email": "new_user@bu.edu",
        "starting_point": "['Your Location', '42.3455898', '-71.0887769']",
        "destination": "['Boston Public Library - Central Library', '42.3493136', '-71.0781875']",
        "places": "['Park', '42.3465259', 'invalid longitude', 'Cafe 939', '42.3481677', '-71.0849947']"
    }
    try:
        add_itinerary_response = client.post(API_path_values.ADD_ITINERARY_PATH, json=data)
        assert add_itinerary_response.status_code == 400
        decoded_response = json.loads(add_itinerary_response.content.decode('utf-8'))
        # print(decoded_response['message'])
        assert decoded_response['status code'] == 400
        assert decoded_response['message'] == "Invalid places format. The amount of information should be multiplication of 3, and each place follows the format of:'PLACE NAME', 'LATITUDE', 'LONGITUDE' "
    except Exception as err:
        traceback.print_exc()
        assert False

def test_add_itinerary_with_empty_string_itinerary_name():
    data = {
        "user_email": "new_user@bu.edu",
        "starting_point": "['Your Location', '42.3455898', '-71.0887769']",
        "destination": "['Boston Public Library - Central Library', '42.3493136', '-71.0781875']",
        "places": "['Park', '42.3465259', '-71.0822474', 'Cafe 939', '42.3481677', '-71.0849947']",
        "itinerary_name": ""
    }
    try:
        add_itinerary_response = client.post(API_path_values.ADD_ITINERARY_PATH, json=data)
        assert add_itinerary_response.status_code == 400
        decoded_response = json.loads(add_itinerary_response.content.decode('utf-8'))
        # print(decoded_response['message'])
        assert decoded_response['status code'] == 400
        assert decoded_response['message'] == "Invalid itinerary name: it can't be an empty string"
    except Exception as err:
        traceback.print_exc()
        assert False


def test_add_itinerary_with_empty_string_created_time():
    data = {
        "user_email": "new_user@bu.edu",
        "starting_point": "['Your Location', '42.3455898', '-71.0887769']",
        "destination": "['Boston Public Library - Central Library', '42.3493136', '-71.0781875']",
        "places": "['Park', '42.3465259', '-71.0822474', 'Cafe 939', '42.3481677', '-71.0849947']",
        "created_time": ""
    }
    try:
        add_itinerary_response = client.post(API_path_values.ADD_ITINERARY_PATH, json=data)
        assert add_itinerary_response.status_code == 422
    except Exception as err:
        traceback.print_exc()
        assert False

def test_add_itinerary_with_invalid_datetime_as_created_time():
    data = {
        "user_email": "new_user@bu.edu",
        "starting_point": "['Your Location', '42.3455898', '-71.0887769']",
        "destination": "['Boston Public Library - Central Library', '42.3493136', '-71.0781875']",
        "places": "['Park', '42.3465259', '-71.0822474', 'Cafe 939', '42.3481677', '-71.0849947']",
        "created_time": "invalid datetime format"
    }
    try:
        add_itinerary_response = client.post(API_path_values.ADD_ITINERARY_PATH, json=data)
        assert add_itinerary_response.status_code == 422
        # decoded_response = json.loads(add_itinerary_response.content.decode('utf-8'))
        # # print(decoded_response['message'])
        # assert decoded_response['status code'] == 400
        # assert decoded_response['message'] == "Invalid created_time format"
    except Exception as err:
        traceback.print_exc()
        assert False


# ========================== for get_a_user_itineraries ==========================
EXISTED_USER_WITH_ITINERARIES = "new_user@bu.edu"
def test_get_a_user_all_itineraries_success():
    try:
        response = client.get(API_path_values.GET_A_USER_ITINERARIES.format(user_email=EXISTED_USER_WITH_ITINERARIES))
        # assert response.status_code == 200
        decoded_response = json.loads(response.content.decode('utf-8'))
        print(decoded_response["message"])
        assert decoded_response["status code"] == 200
        assert decoded_response["message"] == "Successfully get a user's all itineraries"
        assert len(decoded_response['all itineraries']) != 0
    except Exception as err:
        traceback.print_exc()
        assert False




