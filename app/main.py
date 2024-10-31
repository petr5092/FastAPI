from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date
from pydantic import BaseModel
from bookings.router import router as router_book
from users.router import router as router_user
from pages.router import router as router_page


app = FastAPI()

app.include_router(router_user)
app.include_router(router_book)
app.include_router(router_page)










