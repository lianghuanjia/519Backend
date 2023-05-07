from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AddUserItem(BaseModel):
    email: str
    username: str
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    tripPreference: Optional[str] = None

class AddItineraryItem(BaseModel):
    user_email: str
    starting_point: str
    destination: str
    places: Optional[str] = None
    itinerary_name: Optional[str] = None
    created_time: Optional[datetime] = None