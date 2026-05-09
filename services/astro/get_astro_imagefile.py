import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import AltAz, SkyCoord, EarthLocation, get_body, get_sun
from scipy.ndimage import gaussian_filter
from matplotlib.patches import Circle
from const.constellations import CONSTELLATION_LINES
from const.solar_system_bodies import SOLAR_SYSTEM_BODIES;

MAG_LIMIT = 5.8

# ======================================================
# UTIL: HIPs USADOS EM CONSTELAÇÕES
# ======================================================
def get_constellation_hips():
    hips = set()
    for connections in CONSTELLATION_LINES.values():
        for h1, h2 in connections:
            hips.add(int(h1))
            hips.add(int(h2))
    return hips


# ======================================================
# IMAGEM PRINCIPAL
# ======================================================
def generateImageFromCord(
    az_list,
    alt_list,
    width: float,
    height: float,
    loc: EarthLocation,
    time: Time,
    has_constellation_lines: bool,
    has_equatorial_line: bool,
    has_solar_system_bodies: bool,
    mag_list=None,
    hip_list=None
):

    az = az_list.to(u.rad).value
    alt = alt_list.to(u.rad).value

    r = np.tan((np.pi / 2 - alt) / 2)
    r /= np.tan(np.pi / 4)

    x = r * np.sin(az)
    y = r * np.cos(az)

    # ==================================================
    # FILTRO DE POLUIÇÃO VISUAL
    # ==================================================
    if mag_list is not None and hip_list is not None:
        constellation_hips = get_constellation_hips()

        hip_arr = np.array(hip_list, dtype=int)
        mag_arr = np.array(mag_list)

        bright_mask = mag_arr <= MAG_LIMIT
        constellation_mask = np.isin(hip_arr, list(constellation_hips))
        mask = bright_mask | constellation_mask

        x = x[mask]
        y = y[mask]
        alt_list = alt_list[mask]
        mag_list = mag_arr[mask]
        hip_list = hip_arr[mask]

    # ==================================================
    # FIGURA
    # ==================================================
    fig, ax = plt.subplots(figsize=(width, height), dpi=200, facecolor='black')

    if(has_equatorial_line):
        draw_equatorial_grid(ax, time, loc)

    if(has_solar_system_bodies): 
        draw_solar_system(ax, time, loc)

    draw_milky_way(ax, time, loc)

    # ==================================================
    # ESTRELAS (BRILHO AUMENTADO)
    # ==================================================
    # ==================================================
    # ESTRELAS (FRACAS REALÇADAS)
    # ==================================================
    if mag_list is not None:
        base_mag = np.min(mag_list)

        # Curva MAIS SUAVE → favorece estrelas fracas
        sizes = 90 * np.exp(-0.45 * (mag_list - base_mag))
        sizes = np.clip(sizes, 2.5, 120)

        # Identifica estrelas fracas (ex: mag > 3)
        faint_mask = mag_list > (base_mag + 2.5)

        constellation_hips = get_constellation_hips()
        is_constellation_star = np.isin(hip_list, list(constellation_hips))
        sizes[is_constellation_star] *= 1.5

        # =========================
        # HALO DIFERENCIADO
        # =========================
        halo_alpha = np.where(faint_mask, 0.16, 0.08)
        halo_size = np.where(faint_mask, sizes * 4.8, sizes * 3.5)

        ax.scatter(
            x, y,
            s=halo_size,
            color=(0.92, 0.92, 0.92),
            alpha=halo_alpha,
            edgecolors="none",
            zorder=2
        )

        # =========================
        # NÚCLEO
        # =========================
        core_alpha = np.where(faint_mask, 0.85, 0.95)

        ax.scatter(
            x, y,
            s=sizes,
            color="white",
            alpha=core_alpha,
            edgecolors="none",
            zorder=3
        )


    # ==================================================
    # CONSTELAÇÕES
    # ==================================================
    if has_constellation_lines:
        draw_constellation_lines(ax, x, y, hip_numbers=hip_list, alt_rad=alt_list)

    # ==================================================
    # CARDINAIS
    # ==================================================
    ax.text(0, 1.08, 'N', ha='center', va='bottom',
            color='white', fontsize=10, alpha=0.75, fontweight='bold')
    ax.text(0, -1.08, 'S', ha='center', va='top',
            color='white', fontsize=10, alpha=0.75, fontweight='bold')
    ax.text(1.08, 0, 'L', ha='left', va='center',
            color='white', fontsize=10, alpha=0.75, fontweight='bold')
    ax.text(-1.08, 0, 'O', ha='right', va='center',
            color='white', fontsize=10, alpha=0.75, fontweight='bold')

    # ==================================================
    # HORIZONTE
    # ==================================================
    ax.add_patch(
        Circle(
            (0, 0), 1,
            facecolor='none',
            edgecolor='white',
            alpha=0.3,
            linewidth=1.6
        )
    )

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect('equal')
    ax.axis('off')

    fig.savefig("ceu_constelacoes.jpg", dpi=400,
                facecolor="black", bbox_inches='tight', pad_inches=0.05)
    fig.savefig("ceu_constelacoes.tif", dpi=400, format="tiff",
                facecolor="black", bbox_inches='tight', pad_inches=0.05)

    plt.close(fig)


# ======================================================
# CONSTELAÇÕES
# ======================================================
def draw_constellation_lines(ax, x_coords, y_coords, hip_numbers=None, alt_rad=None):
    if hip_numbers is None or len(hip_numbers) == 0:
        return

    hip_to_index = {int(h): i for i, h in enumerate(hip_numbers)}

    for connections in CONSTELLATION_LINES.values():
        for h1, h2 in connections:
            if h1 in hip_to_index and h2 in hip_to_index:
                i1 = hip_to_index[h1]
                i2 = hip_to_index[h2]

                alt_vals = alt_rad.to(u.rad).value
                if alt_vals[i1] < np.radians(-5) or alt_vals[i2] < np.radians(-5):
                    continue

                ax.plot(
                    [x_coords[i1], x_coords[i2]],
                    [y_coords[i1], y_coords[i2]],
                    color='white',
                    alpha=0.7,
                    linewidth=1.4,
                    zorder=4
                )



# ======================================================
# GRADE EQUATORIAL
# ======================================================
def draw_equatorial_grid(ax, time, location):
    grid_color = (0.7, 0.7, 0.7)
    grid_alpha = 0.25
    lw = 0.6

    ra_lines = np.arange(0, 360, 15) * u.deg
    dec_vals = np.linspace(-90, 90, 600) * u.deg

    for ra in ra_lines:
        coords = SkyCoord(
            ra=np.full_like(dec_vals.value, ra.value) * u.deg,
            dec=dec_vals,
            frame="icrs"
        )

        altaz = coords.transform_to(AltAz(obstime=time, location=location))
        mask = altaz.alt > 0 * u.deg
        if np.sum(mask) < 2:
            continue

        alt = altaz.alt[mask].to(u.rad).value
        az = altaz.az[mask].to(u.rad).value

        r = np.tan((np.pi / 2 - alt) / 2)
        r /= np.tan(np.pi / 4)

        ax.plot(
            r * np.sin(az),
            r * np.cos(az),
            color=grid_color,
            alpha=grid_alpha,
            linewidth=lw,
            zorder=0
        )

    dec_lines = np.arange(-60, 90, 15) * u.deg
    ra_vals = np.linspace(0, 360, 800) * u.deg

    for dec in dec_lines:
        coords = SkyCoord(
            ra=ra_vals,
            dec=np.full_like(ra_vals.value, dec.value) * u.deg,
            frame="icrs"
        )

        altaz = coords.transform_to(AltAz(obstime=time, location=location))
        mask = altaz.alt > 0 * u.deg
        if np.sum(mask) < 2:
            continue

        alt = altaz.alt[mask].to(u.rad).value
        az = altaz.az[mask].to(u.rad).value

        r = np.tan((np.pi / 2 - alt) / 2)
        r /= np.tan(np.pi / 4)

        ax.plot(
            r * np.sin(az),
            r * np.cos(az),
            color=grid_color,
            alpha=grid_alpha,
            linewidth=lw,
            zorder=0
        )

def draw_milky_way(ax, time, loc, resolution=500):
    # =========================
    # GRID (imagem)
    # =========================
    img = np.zeros((resolution, resolution))

    # =========================
    # GERAR PONTOS GALÁCTICOS
    # =========================
    n_points = 80000

    l = np.random.uniform(0, 360, n_points) * u.deg
    b = np.random.normal(0, 8, n_points) * u.deg  # largura da banda

    gal = SkyCoord(l=l, b=b, frame="galactic")

    altaz = gal.transform_to(AltAz(obstime=time, location=loc))

    mask = altaz.alt > 0 * u.deg
    if np.sum(mask) < 10:
        return

    alt = altaz.alt[mask].to(u.rad).value
    az = altaz.az[mask].to(u.rad).value

    # =========================
    # SUA PROJEÇÃO
    # =========================
    r = np.tan((np.pi / 2 - alt) / 2)
    r /= np.tan(np.pi / 4)

    x = r * np.sin(az)
    y = r * np.cos(az)

    # =========================
    # MAPEAR PARA PIXEL
    # =========================
    xi = ((x + 1) / 2 * (resolution - 1)).astype(int)
    yi = ((y + 1) / 2 * (resolution - 1)).astype(int)

    valid = (xi >= 0) & (xi < resolution) & (yi >= 0) & (yi < resolution)

    img[yi[valid], xi[valid]] += 1

    # =========================
    # SUAVIZAR → vira "nuvem"
    # =========================
    img = gaussian_filter(img, sigma=6)

    # normalizar
    img = img / img.max()

    # =========================
    # DESENHAR
    # =========================
    ax.imshow(
        img,
        extent=[-1, 1, -1, 1],
        origin="lower",
        cmap="gray",
        alpha=0.1,
        zorder=0
    )


# ======================================================
# SOL E PLANETAS
# ======================================================
def draw_solar_system(ax, time, loc):

    bodies = []

    for name, body_name, color, size in SOLAR_SYSTEM_BODIES:

        # =========================
        # SOL
        # =========================
        if body_name == "sun":
            body = get_sun(time)

        if(body_name == "moon"):
            body = get_body("moon", time, loc)

        # =========================
        # PLANETAS
        # =========================
        else:
            body = get_body(body_name, time, loc)

        body = body.transform_to(
            AltAz(obstime=time, location=loc)
        )

        bodies.append({
            "name": name,
            "coord": body,
            "color": color,
            "size": size
        })

    # =========================
    # DESENHO
    # =========================
    for body in bodies:

        alt = body["coord"].alt
        az = body["coord"].az

        if alt < 0 * u.deg:
            continue

        alt_rad = alt.to(u.rad).value
        az_rad = az.to(u.rad).value

        r = np.tan((np.pi / 2 - alt_rad) / 2)
        r /= np.tan(np.pi / 4)

        x = r * np.sin(az_rad)
        y = r * np.cos(az_rad)

        ax.scatter(
            x,
            y,
            s=body["size"] * 5,
            color=body["color"],
            alpha=0.12,
            edgecolors="none",
            zorder=6
        )

        ax.scatter(
            x,
            y,
            s=body["size"],
            color=body["color"],
            edgecolors="white",
            linewidths=0.5,
            zorder=7
        )