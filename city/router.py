from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from city import crud, schemas
from db.engine import get_db

router = APIRouter(tags=["cities"])


@router.get("/", response_model=List[schemas.City])
async def fetch_all_cities(
        db: AsyncSession = Depends(get_db)
) -> List[schemas.City]:
    cities = await crud.get_all_city(db)
    return cities


@router.post("/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    db_city = await crud.create_city(db=db, city=city)
    return db_city


@router.get("/{city_id}", response_model=schemas.City)
async def fetch_city_by_id(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=404, detail=f"City with id {city_id} not found"
        )
    return db_city


@router.delete("/{city_id}", response_model=schemas.City)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.delete_city_by_id(db, city_id=city_id)
    return db_city


@router.put("/{city_id}/update/", response_model=schemas.City)
async def update_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:
    rows_updated = await crud.update_city(db, city_id, city)
    if rows_updated == 0:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.get_city_by_id(db, city_id)
