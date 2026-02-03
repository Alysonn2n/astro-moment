from fastapi import APIRouter, HTTPException
from schemas.astro_interfaces import AstroDTO
from services.astro.create_astro_moment import createAstroMoment

router = APIRouter()

@router.post("/astro-moment/")
async def create_astro_moment(astro_dto: AstroDTO):
    try:
        createAstroMoment(astro_dto)
        return {
            "message": "Imagem do céu estelar gerada com sucesso",
            "files": [
                "ceu_constelacoes.jpg",
                "ceu_constelacoes.tif"
            ],
            "status": "success"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao processar a imagem: {str(e)}"
        )