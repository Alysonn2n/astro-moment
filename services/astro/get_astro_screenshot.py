import numpy as np
import astropy.units as u
from astropy.coordinates import EarthLocation;
from astropy.time import Time
from astropy.coordinates import AltAz, SkyCoord
from datetime import datetime
from astroquery.vizier import Vizier

# Vizier timeout 
Vizier.TIMEOUT = 120  # 2m

def getSkyFromGeoAndTime(loc: EarthLocation, time: Time):
    v = Vizier(
        columns=["_RAJ2000", "_DEJ2000", "Vmag", "HIP"], 
        row_limit=300000,
    )
    
    try:
        cat = v.query_constraints(catalog="I/239/hip_main")[0]
        
        ra = cat["_RAJ2000"].data * u.deg
        dec = cat["_DEJ2000"].data * u.deg
        mag = np.array(cat["Vmag"])
        hip_numbers = np.array(cat["HIP"])
        
    except Exception as e:
        print(f"Erro: {e}")
        return (
            np.array([]) * u.deg,
            np.array([]) * u.deg,
            np.array([]),
            np.array([], dtype=int)
        )
    
    stars = SkyCoord(ra, dec, frame="icrs")
    altaz = stars.transform_to(AltAz(obstime=time, location=loc))

    visible = altaz.alt > 0*u.deg
    az_visible = altaz.az[visible]
    alt_visible = altaz.alt[visible]
    mag_visible = mag[visible]
    hip_visible = hip_numbers[visible]

    return az_visible, alt_visible, mag_visible, hip_visible