from pydantic import BaseModel
from datetime import date


class SBooking(BaseModel):
    id: int
    rooms_id: int
    users_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    class Confiq:
        orm_mode = True