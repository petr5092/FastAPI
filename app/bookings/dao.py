from bookings.models import Bookings
from dao.base import BaseDAO
from datetime import date
from sqlalchemy import delete, insert, select, func, and_, or_
from database import async_session_maker, engine

from rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        rooms_id: int,
        date_from: date,
        date_to: date
        ):
        """
        WITH booked_rooms AS(
            SELECT * FROM bookings
            WHERE rooms_id = 1 AND
            (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.rooms_id) FROM rooms LEFT JOIN booked_rooms ON booked_rooms.rooms_id = rooms.id WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.rooms_id
        """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.rooms_id == 1,
                    or_(
                        and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_to <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
                )
            ).cte("booked_rooms")
            """
            SELECT rooms.quantity - COUNT(booked_rooms.rooms_id) FROM rooms 
            LEFT JOIN booked_rooms ON booked_rooms.rooms_id = rooms.id 
            WHERE rooms.id = 1
            GROUP BY rooms.quantity, booked_rooms.room id
            """
            rooms_left = select((Rooms.quantity - func.count(booked_rooms.c.rooms_id)
                                ).label("rooms_left")).select_from(Rooms).join(
                                    booked_rooms, booked_rooms.c.rooms_id == Rooms.id
                                ).where(Rooms.id == rooms_id).group_by(
                                    Rooms.quantity, booked_rooms.c.rooms_id
                                )
            print(rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))
            rooms_left = await session.execute(rooms_left)
            print(rooms_left.scalar())
            rooms_left: int = rooms_left.scalar()
            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=rooms_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings). values(
                    room_id=rooms_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ). returning(Bookings)
                new_booking = await session.execute(add_booking)
                return new_booking.scalar() 
            else:
                return None
