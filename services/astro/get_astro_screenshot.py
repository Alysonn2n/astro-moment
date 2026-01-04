from astropy.coordinates import EarthLocation, AltAz, SkyCoord
from astropy.time import Time
from datetime import datetime
from astroquery.vizier import Vizier
import astropy.units as u

def getSkyFromGeoAndTime(lon: float, lat: float, alt: float, dateTime: datetime, referenceStar: str):
    time = Time(dateTime, scale="utc")
    loc = EarthLocation.from_geodetic(lon * u.deg, lat * u.deg, alt * u.m)

    v = Vizier(columns=["_RAJ2000", "_DEJ2000", "Vmag"], row_limit=2000)
    cat = v.query_constraints(catalog="I/239/hip_main", Vmag="<6.5")[0]

    ra = cat["_RAJ2000"].data * u.deg
    dec = cat["_DEJ2000"].data * u.deg
    stars = SkyCoord(ra, dec, frame="icrs")

    altaz = stars.transform_to(AltAz(obstime=time, location=loc))

    # filtra só as que estão acima do horizonte
    visible = altaz.alt > 0*u.deg
    az_visible = altaz.az[visible]
    alt_visible = altaz.alt[visible]


    return az_visible, alt_visible
