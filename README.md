# Astro Moment

API que gera imagens do céu estelar com base em coordenadas geográficas e data/hora, utilizando projeção estereográfica azimutal.

## Exemplo

![Céu estelar](ceu_constelacoes.jpg)

## Funcionalidades

- Renderização do céu visível a partir de qualquer ponto da Terra em qualquer momento
- Linhas de constelações (catálogo Hipparcos via Vizier)
- Grade equatorial (ascensão reta e declinação)
- Corpos do sistema solar (Sol, Lua e planetas)
- Via Láctea (simulação gaussiana)
- Exportação em JPG e TIFF (alta resolução)

## Tecnologias

- Python / FastAPI
- Astropy + Astroquery (catálogo Hipparcos I/239)
- Matplotlib / NumPy / SciPy

## Instalação

```bash
pip install "fastapi[standard]"
pip install "astropy[recommended]" --upgrade
pip install -U --pre "astroquery"
pip install matplotlib scipy numpy
```

Ou via Docker:

```bash
docker build -t astro-moment .
docker run -p 8000:8000 astro-moment
```

## Uso

```bash
fastapi dev
```

### POST /astro-moment/

Gera a imagem do céu estelar.

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

**Parâmetros:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| lat | float | Latitude em graus |
| lon | float | Longitude em graus |
| alt | float | Altitude em metros |
| date_time | datetime | Data e hora (UTC) |
| image.width | float | Largura da imagem (polegadas) |
| image.height | float | Altura da imagem (polegadas) |
| image.has_constellation_lines | bool | Desenhar linhas de constelações |
| image.has_equatorial_lines | bool | Desenhar grade equatorial |
| image.has_solar_system_bodies | bool | Desenhar Sol, Lua e planetas |

**Resposta (200):**

```json
{
  "message": "Imagem do céu estelar gerada com sucesso",
  "files": ["ceu_constelacoes.jpg", "ceu_constelacoes.tif"],
  "status": "success"
}
```

## Estrutura

```
astro-moment/
├── main.py                  # Entrypoint FastAPI
├── controllers/             # Rotas
├── schemas/                 # DTOs (Pydantic)
├── services/astro/          # Lógica de geração
├── const/                   # Constelações e corpos celestes
└── dockerfile
```
