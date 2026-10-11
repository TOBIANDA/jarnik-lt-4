import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.spatial import cKDTree

denah_path = r"c:\Users\kuahs\Documents\Jarnik\final_titik_polos.png"
titik_path = r"c:\Users\kuahs\Documents\Jarnik\kelompok3_L4\output\L4_titik.csv"
ap_fisik_path = r"c:\Users\kuahs\Documents\Jarnik\kelompok3_L4\data\ap_fisik_L4.csv"
out_heatmap = r"c:\Users\kuahs\Documents\Jarnik\kelompok3_L4\output\L4_heatmap.png"
out_status = r"c:\Users\kuahs\Documents\Jarnik\kelompok3_L4\output\L4_status.png"
out_heatmap_under = r"c:\Users\kuahs\Documents\Jarnik\kelompok3_L4\output\_heatmap.png"
out_status_under = r"c:\Users\kuahs\Documents\Jarnik\kelompok3_L4\output\_status.png"

t = pd.read_csv(titik_path)
img = plt.imread(denah_path)
h, w = img.shape[:2]
scale = 22.5  # px/m

# 1. GENERATE HEATMAP
v = t.dropna(subset=["rssi1"])
fig, ax = plt.subplots(figsize=(15, 8.5))
ax.imshow(img)

gx, gy = np.mgrid[0:w:3, 0:h:3]
xy = v[["x_px", "y_px"]].to_numpy(float)
z = v.rssi1.to_numpy(float)

gz = griddata(xy, z, (gx, gy), method="linear")
jarak, _ = cKDTree(xy).query(np.column_stack([gx.ravel(), gy.ravel()]))
gz[(jarak > 6.0 * scale).reshape(gz.shape)] = np.nan

hm = ax.pcolormesh(gx, gy, np.ma.masked_invalid(gz), cmap="RdYlGn", vmin=-90, vmax=-40,
                   alpha=0.62, shading="auto")

fin = gz[np.isfinite(gz)]
lv = [l for l in (-75.0, -67.0) if fin.size and fin.min() < l < fin.max()]
if lv:
    cs = ax.contour(gx, gy, gz, levels=lv, linewidths=1.8, linestyles="--",
                    colors=["#d73027" if l == -75.0 else "#1a9850" for l in lv])
    ax.clabel(cs, fmt="%d dBm", fontsize=9, inline=True)

ax.scatter(t.x_px, t.y_px, c="k", s=14, zorder=4)
for _, r in t.iterrows():
    ax.annotate(f"{r.titik_id}\n{'-' if pd.isna(r.rssi1) else f'{r.rssi1:.0f}'}",
                (r.x_px, r.y_px), fontsize=6.5, xytext=(3, 3), textcoords="offset points", zorder=5)

cb = fig.colorbar(hm, ax=ax, label="RSSI AP terkuat (dBm)", shrink=0.75, pad=0.02)
cb.ax.tick_params(labelsize=10)
ax.set_title("Heatmap RSSI 5 GHz - SSID WiFi-UB.x (interpolasi: linear maks 6 m dari titik)", fontsize=13)
ax.axis("off")
fig.savefig(out_heatmap, dpi=200, bbox_inches="tight")
fig.savefig(out_heatmap_under, dpi=200, bbox_inches="tight")
plt.close(fig)
print("[OK] Heatmap saved with full colors!")

# 2. GENERATE STATUS MAP (NO A1/A2/A3, NO ESTIMASI, ONLY PHYSICAL APs)
WARNA = {"BAIK": "#1a9850", "PERHATIAN": "#fee08b", "BURUK": "#f46d43", "KRITIS": "#a50026"}
fig, ax = plt.subplots(figsize=(15, 8.5))
ax.imshow(img)

# Points by status
for st in ["BAIK", "PERHATIAN", "BURUK", "KRITIS"]:
    s = t[t.status == st]
    if len(s) > 0:
        ax.scatter(s.x_px, s.y_px, c=WARNA[st], s=95, edgecolors="k", lw=0.8,
                   label=f"{st} ({len(s)})", zorder=4)

# Weak areas with clean descriptive names (NO A1/A2/A3)
area_desc = [
    ("L4-002", "Area Depan Toilet"),
    ("L4-012", "Area Teras Luar"),
    ("L4-041", "Area Sayap Barat")
]
kotak = dict(boxstyle="round,pad=0.25", fc="white", ec="#a50026", lw=1, alpha=0.85)
for tid, name in area_desc:
    pt = t[t.titik_id == tid]
    if not pt.empty:
        x, y = pt.iloc[0].x_px, pt.iloc[0].y_px
        ax.add_patch(plt.Circle((x, y), 3 * scale, fc="#d73027", ec="none", alpha=0.2, zorder=2))
        ax.annotate(name, (x, y - 3.2 * scale), fontsize=9, weight="bold", color="#a50026",
                    ha="center", va="center", zorder=6, bbox=kotak)

# Physical APs (6 APs)
if os.path.exists(ap_fisik_path):
    f_ap = pd.read_csv(ap_fisik_path)
    ax.scatter(f_ap.x_px, f_ap.y_px, marker="s", s=130, facecolors="none",
               edgecolors="#08519c", lw=2.2, label="AP Fisik Lantai 4 (6 Unit)", zorder=5)
    
    # Label channel info for APs: ch40, ch161 in core, sayap APs
    labels_ap = {
        "AP-L4-01": "AP Plafon R4.4 (Kanal 40)",
        "AP-L4-02": "AP Plafon R4.3 (Kanal 161)",
        "AP-L4-03": "AP R. Sayap 1",
        "AP-L4-04": "AP R. Sayap 3",
        "AP-L4-05": "AP R. Sayap 4",
        "AP-L4-06": "AP R. Sayap 6",
    }
    kotak_ap = dict(boxstyle="round,pad=0.2", fc="white", ec="#08519c", lw=0.8, alpha=0.85)
    for _, r in f_ap.iterrows():
        lbl = labels_ap.get(r.ap_id, r.ap_id)
        ax.annotate(lbl, (r.x_px, r.y_px), fontsize=7.5, color="#08519c", weight="bold",
                    xytext=(8, -12), textcoords="offset points", zorder=6, bbox=kotak_ap)

ax.scatter([], [], s=180, c="#d73027", alpha=0.25, label="Area Kualitas Lemah")
ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=9.5, frameon=True)
ax.set_title("Peta Status Kualitas Layanan Titik Ukur dan Posisi AP Fisik Lantai 4", fontsize=13)
ax.axis("off")
fig.savefig(out_status, dpi=200, bbox_inches="tight")
fig.savefig(out_status_under, dpi=200, bbox_inches="tight")
plt.close(fig)
print("[OK] Status map saved cleanly without A1/A2/A3!")
