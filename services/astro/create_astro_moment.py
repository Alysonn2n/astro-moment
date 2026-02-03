from schemas.astro_interfaces import AstroDTO
from astropy.coordinates import EarthLocation;
from astropy.time import Time
import astropy.units as u
from .get_astro_imagefile import generateImageFromCord
from .get_astro_screenshot import getSkyFromGeoAndTime

def createAstroMoment(astro_dto: AstroDTO):

    loc = EarthLocation.from_geodetic(astro_dto.lon * u.deg, astro_dto.lat * u.deg, astro_dto.alt * u.m)
    time = Time(astro_dto.date_time, scale="utc")
    az_visible, alt_visible, mag_visible, all_hip_stars = getSkyFromGeoAndTime(
        loc, time
    )

    if alt_visible is None or alt_visible.size == 0:
        raise ValueError("Could not generate image coords")

    generateImageFromCord(
        az_visible,
        alt_visible,
        astro_dto.image.width,
        astro_dto.image.height,
        loc,
        time,
        astro_dto.image.has_constellation_lines,
        mag_visible,
        all_hip_stars
    )
