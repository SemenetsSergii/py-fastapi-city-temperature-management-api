from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from temperature import models, schemas
from city import models as city_models


async def get_temperatures(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10
) -> List[models.Temperature]:
    try:
        result = await db.execute(
            select(models.Temperature).offset(skip).limit(limit)
        )
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise e


async def get_temperature_by_city(
        db: AsyncSession,
        city_id: int,
        skip: int = 0,
        limit: int = 10
) -> List[models.Temperature]:
    try:
        result = await db.execute(
            select(models.Temperature)
            .filter(models.Temperature.city_id == city_id)
            .offset(skip).limit(limit)
        )
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise e


async def create_temperature(
        db: AsyncSession,
        temperature: schemas.TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.dict())
    try:
        db.add(db_temperature)
        await db.commit()
        await db.refresh(db_temperature)
        return db_temperature
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


async def get_cities(db: AsyncSession) -> List[city_models.City]:
    try:
        result = await db.execute(select(city_models.City))
        return result.scalars().all()
    except SQLAlchemyError as e:

        raise e
