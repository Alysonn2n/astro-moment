from fastapi import APIRouter
from schemas.astro_interfaces import AstroDTO
from services.astro.create_astro_moment import createAstroMoment

router = APIRouter()

@router.post("/astro-moment/")
async def create_astro_moment(astroDTO: AstroDTO):
    createAstroMoment(astroDTO)
    return {"message": "Worked"}
