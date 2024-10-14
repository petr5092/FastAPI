from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date
from pydantic import BaseModel


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class SHotel(BaseModel):
    address: str
    name: str
    starts: str


class SHotelSearchArgs:
    def __init__(self,
    location: str,
    date_from: date,
    date_to: date,
    stars: Optional[int] = Query(None, ge=1, le=5 ),
    has_spa: Optional[bool] = None,
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars
        self.has_spa = has_spa


app = FastAPI()


@app.get("/hotels", response_model=list[SHotel])
def get_hotels(
    search_args: SHotelSearchArgs = Depends()
):
    hotels =[
        {
            "address": "sdjf",
            "name": "amama",
            "stars": 5,
        }
    ]
    return search_args


@app.post("/boolings")
def add_booling(booking: SBooking):
    pass

