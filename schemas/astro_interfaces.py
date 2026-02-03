from pydantic import BaseModel
from datetime import datetime

class ImageDTO(BaseModel):
    # inches
    width: float
    height: float
    has_constellation_lines: bool

class AstroDTO(BaseModel):
    lat: float
    lon: float
    # in meters
    alt: float
    date_time: datetime

    image: ImageDTO