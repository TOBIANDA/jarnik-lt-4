import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath
from scipy.interpolate import Rbf
from matplotlib.colors import LinearSegmentedColormap
import os

# Paths
titik_path = r"c:\Users\kuahs\Documents\Jarnik\kelompok3_L4\output\L4_titik.csv"
ap_fisik_path = r"c:\Users\kuahs\Documents\Jarnik\kelompok3_L4\data\ap_fisik_L4.csv"
denah_path = r"c:\Users\kuahs\Documents\Jarnik\final_titik_polos.png"

df_t = pd.read_csv(titik_path)
img = plt.imread(denah_path)
H, W = img.shape[:2]
scale = 22.5  # px per meter

# 1. Building Interior Boundary (Clean polygon covering all rooms & corridors)
poly_main = [
    (670, 130), (910, 130), (910, 70), (1170, 70), (1170, 130),
    (1420, 130), (1420, 420), (1460, 420), (1460, 600), (1420, 600),
    (1420, 890), (1170, 890), (1170, 950), (910, 950), (910, 890),
    (670, 890), (670, 675), (140, 675), (140, 375), (670, 375)
]
interior_path = MplPath(poly_main)

# 2D Grid
gx, gy = np.mgrid[0:W:3, 0:H:3]
pts_grid = np.column_stack([gx.ravel(), gy.ravel()])
mask_interior = interior_path.contains_points(pts_grid).reshape(gx.shape)

grid_pts = pts_grid[mask_interior.ravel()]
n_grid = len(grid_pts)

# 2. Wall Definitions with User's Exact Material Properties
# [((x1, y1), (x2, y2)), material, waf_db]
walls = []

# --- A. Ruangan Sayap Barat ---
# Keliling luar = Batu Bata (~8 dB)
walls.append([np.array([140.0, 375.0]), np.array([670.0, 375.0]), "bata", 8.0])
walls.append([np.array([140.0, 675.0]), np.array([670.0, 675.0]), "bata", 8.0])
walls.append([np.array([140.0, 375.0]), np.array([140.0, 675.0]), "bata", 8.0])
# Pembatas antar ruangan = Batu Bata (~6.5 dB)
walls.append([np.array([315.0, 375.0]), np.array([315.0, 675.0]), "bata", 6.5])
walls.append([np.array([490.0, 375.0]), np.array([490.0, 675.0]), "bata", 6.5])
# Dinding ke arah luar / lorong (yang ada pintu) = Kaca (~2.2 dB)
walls.append([np.array([140.0, 525.0]), np.array([670.0, 525.0]), "kaca", 2.2])

# --- B. Ruangan Titik 28, 31, 32, 30, 06, 33 (Kelas Tengah) ---
# Pembatas antar ruangan = BETON (~13.0 dB)
walls.append([np.array([975.0, 260.0]), np.array([975.0, 470.0]), "beton", 13.0])
walls.append([np.array([1140.0, 260.0]), np.array([1140.0, 470.0]), "beton", 13.0])
walls.append([np.array([975.0, 570.0]), np.array([975.0, 780.0]), "beton", 13.0])
walls.append([np.array([1140.0, 570.0]), np.array([1140.0, 780.0]), "beton", 13.0])
# Pembatas mengarah ke lorong / keluar = KACA (~2.4 dB)
walls.append([np.array([800.0, 260.0]), np.array([1310.0, 260.0]), "kaca", 2.4])
walls.append([np.array([800.0, 470.0]), np.array([1310.0, 470.0]), "kaca", 2.4])
walls.append([np.array([800.0, 570.0]), np.array([1310.0, 570.0]), "kaca", 2.4])
walls.append([np.array([800.0, 780.0]), np.array([1310.0, 780.0]), "kaca", 2.4])
walls.append([np.array([800.0, 260.0]), np.array([800.0, 470.0]), "bata", 6.5])
walls.append([np.array([800.0, 570.0]), np.array([800.0, 780.0]), "bata", 6.5])
walls.append([np.array([1310.0, 260.0]), np.array([1310.0, 470.0]), "bata", 6.5])
walls.append([np.array([1310.0, 570.0]), np.array([1310.0, 780.0]), "bata", 6.5])

# --- C. Ruangan Titik 12 (Utara) & Titik 24 (Selatan) ---
# Titik 12: Keliling batu bata, dinding keluar / pintu kaca
walls.append([np.array([910.0, 70.0]), np.array([910.0, 260.0]), "bata", 6.5])
walls.append([np.array([1170.0, 70.0]), np.array([1170.0, 260.0]), "bata", 6.5])
walls.append([np.array([910.0, 70.0]), np.array([1170.0, 70.0]), "bata", 7.0])
walls.append([np.array([910.0, 260.0]), np.array([1170.0, 260.0]), "kaca", 2.4])

# Titik 24: Keliling batu bata, dinding keluar / pintu kaca
walls.append([np.array([910.0, 780.0]), np.array([910.0, 950.0]), "bata", 6.5])
walls.append([np.array([1170.0, 780.0]), np.array([1170.0, 950.0]), "bata", 6.5])
walls.append([np.array([910.0, 950.0]), np.array([1170.0, 950.0]), "bata", 7.0])
walls.append([np.array([910.0, 780.0]), np.array([1170.0, 780.0]), "kaca", 2.4])

# --- D. Core Lift & Shaft (Beton Masif Bertulang ~18 dB) ---
walls.append([np.array([670.0, 375.0]), np.array([770.0, 375.0]), "beton", 18.0])
walls.append([np.array([770.0, 375.0]), np.array([770.0, 675.0]), "beton", 18.0])
walls.append([np.array([670.0, 675.0]), np.array([770.0, 675.0]), "beton", 18.0])

# --- AP Position: Core APs at Titik 30 & 32, plus 4 APs in sayap ---
aps = [
    {"id": "AP-L4-01", "name": "AP Titik 30", "x": 900.0, "y": 645.0, "ch": "40", "tx": 19.5},
    {"id": "AP-L4-02", "name": "AP Titik 32", "x": 1223.0, "y": 390.0, "ch": "161", "tx": 19.5},
    {"id": "AP-L4-03", "name": "AP Sayap 1", "x": 252.0, "y": 432.0, "ch": "36", "tx": 18.0},
    {"id": "AP-L4-04", "name": "AP Sayap 3", "x": 576.0, "y": 432.0, "ch": "48", "tx": 18.0},
    {"id": "AP-L4-05", "name": "AP Sayap 4", "x": 252.0, "y": 600.0, "ch": "157", "tx": 18.0},
    {"id": "AP-L4-06", "name": "AP Sayap 6", "x": 576.0, "y": 600.0, "ch": "153", "tx": 18.0},
]

# Vectorized Segment Intersect Function
def intersect_vec(A, B, C, D):
    ccw_ACD = (D[1] - A[1]) * (C[0] - A[0]) > (C[1] - A[1]) * (D[0] - A[0])
    ccw_BCD = (D[1] - B[:, 1]) * (C[0] - B[:, 0]) > (C[1] - B[:, 1]) * (D[0] - B[:, 0])
    cond1 = (ccw_ACD != ccw_BCD)
    
    ccw_ABC = (C[1] - A[1]) * (B[:, 0] - A[0]) > (B[:, 1] - A[1]) * (C[0] - A[0])
    ccw_ABD = (D[1] - A[1]) * (B[:, 0] - A[0]) > (B[:, 1] - A[1]) * (D[0] - A[0])
    cond2 = (ccw_ABC != ccw_ABD)
    return cond1 & cond2

print("[*] Melakukan simulasi propagasi gelombang mikro 5 GHz berbasis WAF...")
pl_1m = 46.4
path_loss_exp = 2.85

rssi_ap_grid = []
for ap in aps:
    A = np.array([ap["x"], ap["y"]])
    dx = (grid_pts[:, 0] - ap["x"]) / scale
    dy = (grid_pts[:, 1] - ap["y"]) / scale
    dist_m = np.maximum(np.hypot(dx, dy), 0.75)
    
    pl_base = pl_1m + 10.0 * path_loss_exp * np.log10(dist_m)
    
    waf_total = np.zeros(n_grid)
    for C, D, mat, waf in walls:
        hit = intersect_vec(A, grid_pts, C, D)
        waf_total[hit] += waf
        
    rssi_raw = ap["tx"] - (pl_base + waf_total)
    rssi_ap_grid.append(rssi_raw)

# Max signal received at each location across all APs
rssi_sim_max = np.max(np.array(rssi_ap_grid), axis=0)

# Calibrate model with 43 empirical survey points using Residual RBF
survey_xy = df_t[["x_px", "y_px"]].to_numpy(float)
survey_measured = df_t["rssi1"].to_numpy(float)

survey_sim = []
for sx, sy in survey_xy:
    dists = np.hypot(grid_pts[:, 0] - sx, grid_pts[:, 1] - sy)
    closest_idx = np.argmin(dists)
    survey_sim.append(rssi_sim_max[closest_idx])
survey_sim = np.array(survey_sim)

delta = survey_measured - survey_sim
rbf = Rbf(survey_xy[:, 0], survey_xy[:, 1], delta, function="multiquadric", smooth=1.8)
grid_delta = rbf(grid_pts[:, 0], grid_pts[:, 1])

rssi_final_values = np.clip(rssi_sim_max + grid_delta, -88.0, -34.0)

# Fill 2D matrix
gz_waf = np.full(gx.shape, np.nan)
gz_waf[mask_interior] = rssi_final_values
print("[OK] Selesai menghitung medan sinyal terkalibrasi!")

# -------------------------------------------------------------
# RENDER EKAHAU-STYLE REALISTIC PROPAGATION HEATMAP
# -------------------------------------------------------------
# Ekahau color stops
colors_ekahau = [
    (0.00, "#a50026"),  # Dead zone / below -82 dBm
    (0.20, "#d73027"),  # -78 dBm (Red)
    (0.38, "#f46d43"),  # -74 dBm (Orange)
    (0.52, "#fdae61"),  # -68 dBm (Yellow-Orange)
    (0.66, "#fee08b"),  # -64 dBm (Yellow)
    (0.78, "#a6d96a"),  # -55 dBm (Light Green)
    (0.90, "#66bd63"),  # -46 dBm (Green)
    (1.00, "#1a9850"),  # -35 dBm (Dark Green)
]
cmap_ekahau = LinearSegmentedColormap.from_list("ekahau_rf", [c[1] for c in colors_ekahau])

fig, ax = plt.subplots(figsize=(16, 9.2), dpi=220)
ax.imshow(img)

# Surface plot
hm = ax.pcolormesh(gx, gy, np.ma.masked_invalid(gz_waf), cmap=cmap_ekahau,
                   vmin=-86, vmax=-35, alpha=0.68, shading="gouraud", zorder=2)

# Contours
cs = ax.contour(gx, gy, gz_waf, levels=[-75, -67], colors=["#d73027", "#1a9850"],
                linewidths=[1.8, 2.2], linestyles=["--", "-"], zorder=3)
ax.clabel(cs, fmt="%d dBm", fontsize=9.5, inline=True)

# Survey Points
ax.scatter(df_t.x_px, df_t.y_px, c="black", s=13, zorder=5)
for _, r in df_t.iterrows():
    ax.annotate(f"{r.titik_id}\n{r.rssi1:.0f}", (r.x_px, r.y_px),
                fontsize=6.2, xytext=(3, 3), textcoords="offset points", zorder=6,
                color="#111111", weight="medium")

# AP Markers (Ekahau Style: White circular badge with red dashed ring and channel)
for ap in aps:
    # Outer ring
    c_ring = plt.Circle((ap["x"], ap["y"]), 24, fill=False, color="#d73027",
                        linestyle="--", linewidth=2.5, zorder=8)
    # Inner badge
    c_bg = plt.Circle((ap["x"], ap["y"]), 20, fill=True, facecolor="white",
                      edgecolor="#222222", linewidth=1.2, zorder=9)
    ax.add_patch(c_ring)
    ax.add_patch(c_bg)
    ax.text(ap["x"], ap["y"], ap["ch"], fontsize=9.5, weight="bold",
            color="#a50026", ha="center", va="center", zorder=10)

# Colorbar
cb = fig.colorbar(hm, ax=ax, shrink=0.74, pad=0.02, aspect=26)
cb.set_label("Kuat Sinyal RSSI 5 GHz (dBm)", fontsize=11, weight="bold")
cb.ax.tick_params(labelsize=10)

ax.set_title("Heatmap Propagasi Gelombang Mikro & Redaman Dinding (WAF) 5 GHz — Lantai 4",
             fontsize=14, weight="bold", pad=12)
ax.axis("off")

# Save outputs
out_png = r"c:\Users\kuahs\Documents\Jarnik\kelompok3_L4\output\L4_heatmap.png"
out_png_under = r"c:\Users\kuahs\Documents\Jarnik\kelompok3_L4\output\_heatmap.png"
fig.savefig(out_png, bbox_inches="tight", dpi=200)
fig.savefig(out_png_under, bbox_inches="tight", dpi=200)
plt.close(fig)

print(f"[SUCCESS] Heatmap Ekahau-style WAF berhasil disimpan ke: {out_png}")
