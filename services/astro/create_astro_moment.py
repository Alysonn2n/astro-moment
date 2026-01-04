from schemas.astro_interfaces import AstroDTO
from .get_astro_imagefile import generateImageFromCord
from .get_astro_screenshot import getSkyFromGeoAndTime

def createAstroMoment(astroDTO: AstroDTO):
    az_visible, alt_visible = getSkyFromGeoAndTime(
        astroDTO.lon, astroDTO.lat, astroDTO.alt,
        astroDTO.dateTime, astroDTO.referenceStar
    )

    if alt_visible is None or alt_visible.size == 0:
        raise ValueError("Could not generate image coords")

    generateImageFromCord(
        az_visible, alt_visible,
        astroDTO.image.width, astroDTO.image.height
    )
