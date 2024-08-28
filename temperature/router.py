import asyncio
import httpx
import os

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from dotenv import load_dotenv

from temperature import crud, schemas
from db.engine import get_db

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

router = APIRouter(tags=["temperatures"])


async def fetch_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"http://api.weatherapi.com/v1/current.json?key="
                f"{API_KEY}&q={city_name}"
            )
            response.raise_for_status()
            data = response.json()
            return data["current"]["temp_c"]
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error fetching temperature: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch temperature: {str(e)}"
            )


@router.get("/", response_model=List[schemas.Temperature])
async def fetch_all_temperatures(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)
) -> List[schemas.Temperature]:
    temperatures = await crud.get_temperatures(db, skip=skip, limit=limit)
    return temperatures


@router.get("/city/{city_id}/", response_model=List[schemas.Temperature])
async def fetch_temperatures_by_city(
        city_id: int,
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)
) -> List[schemas.Temperature]:
    temperatures = await crud.get_temperature_by_city(
        db, city_id=city_id,
        skip=skip,
        limit=limit
    )
    return temperatures


@router.post("/update/", response_model=List[schemas.Temperature])
async def update_temperatures(
        db: AsyncSession = Depends(get_db)
) -> List[schemas.Temperature]:
    cities = await crud.get_cities(db)
    temperatures = []

    async def fetch_and_store(city) -> schemas.Temperature:
        temperature = await fetch_temperature(city.name)
        db_temperature = schemas.TemperatureCreate(
            city_id=city.id, date_time=datetime.now(), temperature=temperature
        )
        return await crud.create_temperature(db, db_temperature)

    tasks = [fetch_and_store(city) for city in cities]
    temperatures = await asyncio.gather(*tasks)
    return temperatures
