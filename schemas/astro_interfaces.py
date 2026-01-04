from pydantic import BaseModel
from datetime import datetime

class ImageDTO(BaseModel):
    # inches
    width: float
    height: float

class AstroDTO(BaseModel):
    lat: float
    lon: float
    # in meters
    alt: float
    dateTime: datetime
    referenceStar: str

    image: ImageDTO