from typing import List, Optional

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from city import models, schemas


async def get_all_city(db: AsyncSession) -> List[models.City]:
    try:
        result = await db.execute(select(models.City))
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_city_by_name_and_info(
    db: AsyncSession, name: str, additional_info: str
) -> Optional[models.City]:
    try:
        result = await db.execute(
            select(models.City)
            .filter(
                models.City.name == name,
                models.City.additional_info == additional_info
            )
        )
        return result.scalars().first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.City(**city.dict())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_city_by_id(
        db: AsyncSession,
        city_id: int
) -> Optional[models.City]:
    try:
        result = await db.execute(
            select(models.City)
            .filter(models.City.id == city_id)
        )
        return result.scalars().first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_city_by_id(db: AsyncSession, city_id: int) -> models.City:
    try:
        db_city = await get_city_by_id(db, city_id)
        if db_city is None:
            raise HTTPException(status_code=404, detail="City not found")
        await db.delete(db_city)
        await db.commit()
        return db_city
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_city(
        db: AsyncSession,
        city_id: int,
        city_update: schemas.CityUpdate
) -> int:
    try:
        query = (
            update(models.City)
            .where(models.City.id == city_id)
            .values(
                name=city_update.name,
                additional_info=city_update.additional_info
            )
            .execution_options(synchronize_session="fetch")
        )
        result = await db.execute(query)
        await db.commit()
        return result.rowcount
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
