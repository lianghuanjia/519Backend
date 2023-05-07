from traceback import print_exc
from schemas import AddUserItem, AddItineraryItem
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from util import user_exists, delete_user_in_database
from database_table_definition import User, Itinerary
from database import get_session

app = FastAPI()

HTTPResponse_400_DETAIL = {
    "INVALID_STARTING_POINT":{"status code":400, "message":"Starting point has incorrect format. It needs to be in this format: "}
}


@app.post("/user/add-user/")
def add_user_to_database(item: AddUserItem):
    try:
        if item.email == "":
            return JSONResponse(status_code=400, content={'message':'Missing user email'})
        if item.username == "":
            return JSONResponse(status_code=400, content={'message': 'Missing username'})
        if user_exists(item.email):
            return JSONResponse(status_code=400, content={'message': 'User exists already'})
        new_user = User(email=item.email, username=item.username, phone=item.phone, age=item.age, gender=item.gender,
                        tripPreference=item.tripPreference)
        db_session = get_session()
        db_session.add(new_user)
        db_session.commit()
        return JSONResponse(status_code=200, content={'message': 'Add user successfully'})
    except Exception as e:
        print_exc()
        delete_user_in_database(item.email)
        raise HTTPException(status_code=500, detail='Internal Error')





def check_place_format(location):
    pass

@app.post("/itinerary/add-itinerary/")
def add_itinerary_to_database(item: AddItineraryItem):
    try:
        if item.user_email == "":
            return JSONResponse(status_code=400, content={'message': 'Missing user email'})
        if item.starting_point == "":
            return JSONResponse(status_code=400, content={'message': 'Missing starting point'})
        if not check_place_format(item.starting_point):
            return JSONResponse(status_code=400, content={'message'})
        if item.destination == "":
            return JSONResponse(status_code=400, content={'message': 'Missing destination'})
        new_itinerary = Itinerary(user_email=item.user_email,starting_point=item.starting_point,destination=item.destination,places=item.places, itinerary_name=item.itinerary_name, created_time=item.created_time)
        db_session = get_session()
        db_session.add(new_itinerary)
        db_session.commit()
        return JSONResponse(status_code=200, content={'message': 'Add itinerary successfully'})
    except Exception as e:
        print_exc()
        delete_user_in_database(item.user_email)
        raise HTTPException(status_code=500, detail='Internal Error')