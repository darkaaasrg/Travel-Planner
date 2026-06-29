import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models import Place, Project
from app.schemas import PlaceCreate, PlaceUpdate, PlaceOut
from app.services.artic import get_artwork_from_api

router = APIRouter(prefix="/projects/{project_id}/places", tags=["places"])


async def fetch_place_from_external_api(external_id: int):
    url = f"https://api.artic.edu/api/v1/artworks/{external_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            if response.status_code == 200:
                data = response.json().get("data", {})
                return {
                    "title": data.get("title"),
                    "artist": data.get("artist_display"),
                    "image_url": (
                        f"https://www.artic.edu/iiif/2/{data.get('image_id')}/full/843,/0/default.jpg"
                        if data.get("image_id")
                        else None
                    ),
                }
        except Exception:
            return None
    return None


@router.post("/", response_model=PlaceOut, status_code=status.HTTP_201_CREATED)
async def add_place(
    project_id: int, data: PlaceCreate, db: AsyncSession = Depends(get_db)
):
    project = (
        await db.execute(select(Project).filter(Project.id == project_id))
    ).scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    artwork_data = await get_artwork_from_api(data.external_id)
    if not artwork_data:
        raise HTTPException(
            status_code=400, detail="Place (artwork) not found in external API"
        )

    new_place = Place(**data.model_dump(), **artwork_data, project_id=project_id)
    db.add(new_place)
    await db.commit()
    await db.refresh(new_place)
    return new_place


@router.get("/", response_model=list[PlaceOut])
async def list_places(project_id: int, db: AsyncSession = Depends(get_db)):
    return (
        (await db.execute(select(Place).filter(Place.project_id == project_id)))
        .scalars()
        .all()
    )


@router.get("/{place_id}", response_model=PlaceOut)
async def get_place(project_id: int, place_id: int, db: AsyncSession = Depends(get_db)):
    place = (
        await db.execute(
            select(Place).filter(Place.id == place_id, Place.project_id == project_id)
        )
    ).scalar_one_or_none()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@router.patch("/{place_id}", response_model=PlaceOut)
async def update_place(
    project_id: int,
    place_id: int,
    data: PlaceUpdate,
    db: AsyncSession = Depends(get_db),
):
    place = (
        await db.execute(
            select(Place).filter(Place.id == place_id, Place.project_id == project_id)
        )
    ).scalar_one_or_none()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(place, key, value)

    await db.commit()
    await db.refresh(place)
    return place
