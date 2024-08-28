from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from city import models, schemas


async def get_all_city(db: AsyncSession) -> List[models.City]:
    result = await db.execute(select(models.City))
    return result.scalars().all()


async def get_city_by_name_and_info(
    db: AsyncSession, name: str, additional_info: str
) -> Optional[models.City]:
    result = await db.execute(
        select(models.City).filter(models.City.name == name, models.City.additional_info == additional_info)
    )
    return result.scalars().first()


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    db_city = await get_city_by_name_and_info(db, city.name, city.additional_info)
    if db_city:
        raise HTTPException(
            status_code=400,
            detail="Such name and additional info for city already exists",
        )
    new_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)

    return new_city


async def get_city_by_id(db: AsyncSession, city_id: int) -> Optional[models.City]:
    result = await db.execute(select(models.City).filter(models.City.id == city_id))
    return result.scalars().first()


async def delete_city_by_id(db: AsyncSession, city_id: int) -> models.City:
    db_city = await get_city_by_id(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    await db.delete(db_city)
    await db.commit()
    return db_city


async def update_city(db: AsyncSession, city_id: int, city_update: schemas.CityUpdate) -> int:
    query = (
        update(models.City)
        .where(models.City.id == city_id)
        .values(name=city_update.name, additional_info=city_update.additional_info)
        .execution_options(synchronize_session="fetch")
    )
    result = await db.execute(query)
    await db.commit()
    return result.rowcount