# Astro Moment

API that generates star sky images based on geographic coordinates and date/time, using azimuthal stereographic projection

## Example

![Star sky](ceu_constelacoes.jpg)

## Features

- Rendering of the visible sky from any point on Earth at any time
- Constellation lines (Hipparcos catalog via Vizier)
- Equatorial grid (right ascension and declination)
- Solar system bodies (Sun, Moon and planets)
- Milky Way (Gaussian simulation)
- Export in JPG and TIFF (high resolution)

## Technologies

- Python / FastAPI
- Astropy + Astroquery (Hipparcos catalog I/239)
- Matplotlib / NumPy / SciPy

## Installation

```bash
pip install "fastapi[standard]"
pip install "astropy[recommended]" --upgrade
pip install -U --pre "astroquery"
pip install matplotlib scipy numpy
```

Or via Docker:

```bash
docker build -t astro-moment .
docker run -p 8000:8000 astro-moment
```

## Usage

```bash
fastapi dev
```

### POST /astro-moment/

Generates the star sky image.

**Request body:**

```json
{
  "lat": -23.55,
  "lon": -46.63,
  "alt": 760,
  "date_time": "2024-06-15T22:00:00",
  "image": {
    "width": 10.0,
    "height": 10.0,
    "has_constellation_lines": true,
    "has_equatorial_lines": true,
    "has_solar_system_bodies": true
  }
}
```

**Parameters:**

| Field | Type | Description |
|-------|------|-------------|
| lat | float | Latitude in degrees |
| lon | float | Longitude in degrees |
| alt | float | Altitude in meters |
| date_time | datetime | Date and time (UTC) |
| image.width | float | Image width (inches) |
| image.height | float | Image height (inches) |
| image.has_constellation_lines | bool | Draw constellation lines |
| image.has_equatorial_lines | bool | Draw equatorial grid |
| image.has_solar_system_bodies | bool | Draw Sun, Moon and planets |

**Response (200):**

```json
{
  "message": "Star sky image generated successfully",
  "files": ["ceu_constelacoes.jpg", "ceu_constelacoes.tif"],
  "status": "success"
}
```

## Structure

```
astro-moment/
├── main.py                  # FastAPI entrypoint
├── controllers/             # Routes
├── schemas/                 # DTOs (Pydantic)
├── services/astro/          # Generation logic
├── const/                   # Constellations and celestial bodies
└── dockerfile
```
