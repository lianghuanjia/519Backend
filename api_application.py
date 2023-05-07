from traceback import print_exc
from schemas import AddUserItem, AddItineraryItem
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from util import user_exists, delete_user_in_database
from database_table_definition import User, Itinerary
from database import get_session
from itinerary import check_one_place_format, check_places_format, check_datetime

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
    "INVALID_DATETIME":{"status code":400, "message":"Invalid created_time format."}
}

Itinerary_HTTPResponse_200_DETAIL = {
    "Add_ITINERARY_SUCCESS": {"status code": 200, "message":"Added itinerary successfully"}
}


@app.post("/itinerary/add-itinerary/")
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
        if item.created_time != "" or item.created_time is not None:
            if not check_datetime(item.created_time):
                return JSONResponse(status_code=400, content=Itinerary_HTTPResponse_400_DETAIL["INVALID_DATETIME"])
        new_itinerary = Itinerary(user_email=item.user_email,starting_point=item.starting_point,destination=item.destination,places=item.places, itinerary_name=item.itinerary_name, created_time=item.created_time)
        db_session = get_session()
        db_session.add(new_itinerary)
        db_session.commit()
        return JSONResponse(status_code=200, content=Itinerary_HTTPResponse_200_DETAIL["Add_ITINERARY_SUCCESS"])
    except Exception as e:
        print_exc()
        raise HTTPException(status_code=500, detail='Internal Error')