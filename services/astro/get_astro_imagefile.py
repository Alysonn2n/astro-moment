import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u

def generateImageFromCord(az_list, alt_list, width, height):
    # Converter para radianos
    az = az_list.to(u.rad).value
    alt = alt_list.to(u.rad).value
    
    # Projeção estereográfica
    r = np.tan((np.pi/2 - alt)/2)
    
    # Normalize so horizon is at radius 1
    max_r = np.tan(np.pi/4)  # = 1.0
    r = r / max_r
    
    # Coordenadas cartesianas
    x = r * np.sin(az)
    y = r * np.cos(az)
    
    # DEBUG: Check if data is valid
    print(f"Number of stars: {len(x)}")
    print(f"x range: [{np.min(x):.3f}, {np.max(x):.3f}]")
    print(f"y range: [{np.min(y):.3f}, {np.max(y):.3f}]")
    print(f"r range: [{np.min(r):.3f}, {np.max(r):.3f}]")
    print(f"alt range (degrees): [{np.min(alt)*180/np.pi:.1f}, {np.max(alt)*180/np.pi:.1f}]")
    
    # If stars are still off-center, you might need to center them manually
    # This centers the distribution by subtracting the centroid
    centroid_x, centroid_y = np.mean(x), np.mean(y)
    print(f"Centroid before centering: ({centroid_x:.3f}, {centroid_y:.3f})")
    
    # Only apply centering if it's significantly off-center
    if abs(centroid_x) > 0.1 or abs(centroid_y) > 0.1:
        x = x - centroid_x
        y = y - centroid_y
        
        # After centering, we need to ensure all points are within the circle
        # by rescaling if necessary
        distances = np.sqrt(x**2 + y**2)
        max_distance = np.max(distances)
        if max_distance > 1.0:
            x = x / max_distance
            y = y / max_distance
    
    # Create figure
    fig, ax = plt.subplots(figsize=(width, height), dpi=100)
    ax.scatter(x, y, s=1, color="white", alpha=0.8)
    
    # Draw horizon circle
    circle = plt.Circle((0, 0), 1, fill=False, color='gray', linestyle='--', alpha=0.3, linewidth=0.5)
    ax.add_artist(circle)
    
    # Mark the cardinal directions
    ax.text(0, 1.05, 'N', ha='center', va='bottom', color='gray', fontsize=8)
    ax.text(0, -1.05, 'S', ha='center', va='top', color='gray', fontsize=8)
    ax.text(1.05, 0, 'E', ha='left', va='center', color='gray', fontsize=8)
    ax.text(-1.05, 0, 'W', ha='right', va='center', color='gray', fontsize=8)
    
    # Limites do círculo
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect('equal')
    ax.set_facecolor("black")
    ax.axis('off')
    
    # Salvar imagens
    fig.savefig("ceu_constelacoes.jpg", dpi=300, facecolor="black", bbox_inches='tight', pad_inches=0)
    fig.savefig("ceu_constelacoes.tif", dpi=300, format="tiff", facecolor="black", bbox_inches='tight', pad_inches=0)
    plt.close(fig)