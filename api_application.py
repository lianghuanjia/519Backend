from traceback import print_exc

import util
from schemas import AddUserItem, AddItineraryItem
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from util import user_exists, delete_user_in_database
from database_table_definition import User, Itinerary
from database import get_session
from itinerary import check_one_place_format, check_places_format, check_datetime
import API_path_values


app = FastAPI()

User_HTTPResponse_400_DETAIL = {
    "INVALID_STARTING_POINT":{"status code":400, "message":"Starting point has incorrect format. It needs to be in this format: "},
    "MISSING_EMAIL":{"status code":400, "message":"Missing required field: user email"},
    "MISSING_USERNAME":{"status code":400, "message":"Missing required field: username"},
    "USER_EXISTS_ALREADY":{"status code":400, "message":"User exists already"}
}

User_HTTPResponse_200_DETAIL = {
    "Add_ITINERARY_SUCCESS":{"status code":200, "message":"Added itinerary successfully"}
}



@app.post("/user/add-user/")
def add_user_to_database(item: AddUserItem):
    try:
        if item.email == "":
            return JSONResponse(status_code=400, content=User_HTTPResponse_400_DETAIL["MISSING_EMAIL"])
        if item.username == "":
            return JSONResponse(status_code=400, content=User_HTTPResponse_400_DETAIL["MISSING_USERNAME"])
        if user_exists(item.email):
            return JSONResponse(status_code=400, content=User_HTTPResponse_400_DETAIL["USER_EXISTS_ALREADY"])
        new_user = User(email=item.email, username=item.username, phone=item.phone, age=item.age, gender=item.gender,
                        tripPreference=item.tripPreference)
        db_session = get_session()
        db_session.add(new_user)
        db_session.commit()
        return JSONResponse(status_code=200, content=User_HTTPResponse_200_DETAIL["Add_ITINERARY_SUCCESS"])
    except Exception as e:
        print_exc()
        delete_user_in_database(item.email)
        raise HTTPException(status_code=500, detail='Internal Error')

#"":{"status code": 400,"message":""},

Itinerary_HTTPResponse_400_DETAIL = {
    "MISSING_USER_EMAIL":{"status code": 400,"message":"Missing field: user email"},
    "MISSING_STARTING_POINT":{"status code": 400,"message":"Missing field: starting point"},
    "MISSING_DESTINATION":{"status code": 400, "message":"Missing field: destination"},
    "MISSING_PLACE(S)": {"status code":400, "message":"Missing field: places"},
    "INVALID_STARTING_POINT_FORMAT":{"status code":400, "message":"Invalid starting point format. It should be: ['PLACE NAME', 'LATITUDE', 'LONGITUDE']"},
    "INVALID_DESTINATION_FORMAT":{"status code":400,"message":"Invalid destination format. It should be: ['PLACE NAME', 'LATITUDE', 'LONGITUDE']"},
    "INVALID_PLACES_FORMAT":{"status code":400, "message":"Invalid places format. The amount of information should be multiplication of 3, and each place follows the format of:'PLACE NAME', 'LATITUDE', 'LONGITUDE' "},
    "INVALID_DATETIME_FORMAT":{"status code":400, "message":"Invalid created_time format"},
    "INVALID_ITINERARY_NAME": {"status code":400, "message":"Invalid itinerary name: it can't be an empty string"},
    "INVALID_DATETIME_EMPTY_STRING":{"status code":400, "message":"Invalid created_time: it can't be an empty string"},
    "SINGLE_ITINERARY_NOT_FOUND":{"status code":400, "message":"Single itinerary not found"},
    "NO_DISPLAY_RESULT": {"status code": 400, "message": "Unable to calculate optimized solution"}
}

Itinerary_HTTPResponse_200_DETAIL = {
    "Add_ITINERARY_SUCCESS": {"status code": 200, "message":"Added itinerary successfully"},
    "GET_A_USER_ITINERARIES_SUCCESS":{"status code": 200, "message":"Successfully get a user's all itineraries"},
    "USER_HAS_NO_ITINERARY": {"status code": 201, "message": "User has no itinerary"},
    "GET_ITINERARY__OPTIMIZED_ROUTE_SUCCESS": {"status code":200, "message":"Successfully get an itinerary's optimized route"}
}


@app.post(API_path_values.ADD_ITINERARY_PATH)
def add_itinerary_to_database(item: AddItineraryItem):
    try:
        if item.user_email == "":
            return JSONResponse(status_code=400, content=Itinerary_HTTPResponse_400_DETAIL["MISSING_USER_EMAIL"])
        if item.starting_point == "":
            return JSONResponse(status_code=400, content=Itinerary_HTTPResponse_400_DETAIL["MISSING_STARTING_POINT"])
        if item.destination == "":
            return JSONResponse(status_code=400, content=Itinerary_HTTPResponse_400_DETAIL["MISSING_DESTINATION"])
        if item.places == "":
            return JSONResponse(status_code=400, content=Itinerary_HTTPResponse_400_DETAIL["MISSING_PLACE(S)"])
        if not check_one_place_format(item.starting_point):
            return JSONResponse(status_code=400, content=Itinerary_HTTPResponse_400_DETAIL["INVALID_STARTING_POINT_FORMAT"])
        if not check_one_place_format(item.destination):
            return JSONResponse(status_code=400, content=Itinerary_HTTPResponse_400_DETAIL["INVALID_DESTINATION_FORMAT"])
        if not check_places_format(item.places):
            return JSONResponse(status_code=400, content=Itinerary_HTTPResponse_400_DETAIL["INVALID_PLACES_FORMAT"])
        if item.itinerary_name == "":
            return JSONResponse(status_code=400, content=Itinerary_HTTPResponse_400_DETAIL["INVALID_ITINERARY_NAME"])
        if item.created_time is not None:
            if item.created_time == "":
                return JSONResponse(status_code=400, content=Itinerary_HTTPResponse_400_DETAIL["INVALID_DATETIME_EMPTY_STRING"])
            if not check_datetime(item.created_time):
                return JSONResponse(status_code=400, content=Itinerary_HTTPResponse_400_DETAIL["INVALID_DATETIME_FORMAT"])
        new_itinerary = Itinerary(user_email=item.user_email,starting_point=item.starting_point,destination=item.destination,places=item.places, itinerary_name=item.itinerary_name, created_time=item.created_time)
        db_session = get_session()
        db_session.add(new_itinerary)
        db_session.flush()
        db_session.commit()
        db_session.refresh(new_itinerary)
        add_itinerary_success_response = Itinerary_HTTPResponse_200_DETAIL["Add_ITINERARY_SUCCESS"]
        add_itinerary_success_response["itinerary_id"] = new_itinerary.id
        return JSONResponse(status_code=200, content=add_itinerary_success_response)
    except Exception as e:
        print_exc()
        raise HTTPException(status_code=500, detail='Internal Error')




@app.get(API_path_values.GET_A_USER_ITINERARIES)
def get_a_user_itineraries(user_email: str):
    try:
        all_itineraries = util.get_a_user_itineraries_from_database(user_email)
        return_payload = util.process_a_user_all_itineraries_response(all_itineraries)
        if not return_payload:
            return JSONResponse(status_code=201, content=Itinerary_HTTPResponse_200_DETAIL["USER_HAS_NO_ITINERARY"])
        else:
            return_response = Itinerary_HTTPResponse_200_DETAIL["GET_A_USER_ITINERARIES_SUCCESS"]
            return_response["all itineraries"] = return_payload
            return JSONResponse(status_code=200, content=return_response)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail='Internal Error')


@app.get(API_path_values.GET_ONE_ITINERARY)
def get_one_itinerary_and_its_optimized_path(str_itinerary_id: str, travel_mode: str):
    try:
        itinerary_id = int(str_itinerary_id)
        itinerary = util.get_an_itinerary_from_database(itinerary_id)
        if itinerary is None:
            return JSONResponse(status_code=400, content=Itinerary_HTTPResponse_400_DETAIL["SINGLE_ITINERARY_NOT_FOUND"])
        # print(itinerary_id)
        # print(travel_mode)
        # print(itinerary)
        display_result = util.get_optimized_order(travel_mode, itinerary)
        if not display_result:
            return JSONResponse(status_code=400, content=Itinerary_HTTPResponse_400_DETAIL["NO_DISPLAY_RESULT"])
        else:
            return_content = Itinerary_HTTPResponse_200_DETAIL["GET_ITINERARY__OPTIMIZED_ROUTE_SUCCESS"]
            return_content["route"] = display_result
            return JSONResponse(status_code=200, content=return_content)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail='Internal Error')
