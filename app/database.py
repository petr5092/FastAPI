from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import as_declarative
import datetime
from confiq import settings

def get_current_datetime():
    return datetime.datetime.utcnow()


@as_declarative()
class Base:
    id = Column(
        Integer,
        primary_key=True,
    )

    created_at = Column(
        DateTime,
        default=get_current_datetime,
    )

    updated_at = Column(
        DateTime,
        default=get_current_datetime,
        onupdate=get_current_datetime,
    )


engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


