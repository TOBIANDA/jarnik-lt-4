import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as pe
import numpy as np
import pandas as pd
from PIL import Image
import os

BASE_DIR = r'c:\Users\kuahs\Documents\Jarnik\kelompok3_L4'
DENAH_DIR = os.path.join(BASE_DIR, 'denah')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Load clean image
clean_path = os.path.join(BASE_DIR, 'final_clean.png')
if not os.path.exists(clean_path):
    clean_path = r'c:\Users\kuahs\Documents\Jarnik\final_clean.png'
im_clean = Image.open(clean_path).convert('RGB')
W, H = im_clean.size

# Structural coordinates in final.jpeg:
ORIGIN_X_SUMBU_F = 658
ORIGIN_Y_SUMBU_6 = 276
SCALE_M = 22.5  # px per meter (162 px / 7.2m)

grid_cols = {
    'W3': 170, 'W2': 333, 'W1': 495,
    'F': 658, 'E': 819, 'D': 980, 'C': 1146, 'B': 1300, 'A': 1362
}

grid_rows = {
    '6': 276, '5': 444, '4': 601, '3': 760
}

# Load points from data/titik_L4.csv
df_pts = pd.read_csv(os.path.join(DATA_DIR, 'titik_L4.csv'))

fig, ax = plt.subplots(figsize=(16, 10.35), dpi=100)
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis('off')

ax.imshow(im_clean)

# Title
ax.text(W / 2, 28, "GEDUNG F FILKOM UB — LANTAI 4 (SKETSA KARTESIUS & GRID STRUKTURAL)",
        fontsize=11.5, fontweight='heavy', ha='center', color='#0f172a', zorder=25,
        bbox=dict(boxstyle='square,pad=0.25', fc='white', ec='#cbd5e1', lw=0.8))

c_centerline = '#cbd5e1'
c_axis_bubble = '#1d4ed8'
halo_point = [pe.withStroke(linewidth=2.4, foreground='white')]
halo_cal = [pe.withStroke(linewidth=2.8, foreground='white')]

# 1. Structural Axis Lines & Grid Bubbles
out_x1, out_y1 = 657, 71
out_w, out_h = 1500 - 657, 962 - 71

for name, x in grid_cols.items():
    ax.plot([x, x], [out_y1, out_y1 + out_h], color=c_centerline, linestyle='-.', linewidth=0.7, alpha=0.55, zorder=3)
    # Bubble tag on top border
    ax.add_patch(patches.Circle((x, out_y1), 10.5, facecolor='#eff6ff', edgecolor=c_axis_bubble, linewidth=1.3, zorder=12))
    ax.text(x, out_y1, name, fontsize=7.5, fontweight='bold', color=c_axis_bubble, ha='center', va='center', zorder=13)

for name, y in grid_rows.items():
    ax.plot([170, 1500], [y, y], color=c_centerline, linestyle='-.', linewidth=0.7, alpha=0.55, zorder=3)
    # Bubble tag on right border
    ax.add_patch(patches.Circle((1500, y), 10.5, facecolor='#eff6ff', edgecolor=c_axis_bubble, linewidth=1.3, zorder=12))
    ax.text(1500, y, name, fontsize=7.5, fontweight='bold', color=c_axis_bubble, ha='center', va='center', zorder=13)

# 2. Metric Ruler along top border (Meters from Sumbu F)
for m in range(-20, 36, 5):
    x_pos = ORIGIN_X_SUMBU_F + m * SCALE_M
    if 200 <= x_pos <= 1490:
        ax.plot([x_pos, x_pos], [out_y1 - 4, out_y1], color='#334155', linewidth=1.1, zorder=11)
        ax.text(x_pos, out_y1 - 6, f"{m:+d}m" if m != 0 else "0m", fontsize=6.2, color='#1e293b', fontweight='bold',
                ha='center', va='bottom', zorder=11)

# Left ruler along Y (Meters from Sumbu 6)
for m in range(-5, 31, 5):
    y_pos = ORIGIN_Y_SUMBU_6 + m * SCALE_M
    if out_y1 + 10 <= y_pos <= out_y1 + out_h - 10:
        ax.plot([170 - 4, 170], [y_pos, y_pos], color='#334155', linewidth=1.1, zorder=11)
        ax.text(170 - 6, y_pos, f"{m:+d}m" if m != 0 else "0m", fontsize=6.2, color='#1e293b', fontweight='bold',
                ha='right', va='center', zorder=11)

# Subtle axis coordinate labels in margins (cleanly placed away from ticks)
ax.text(90, out_y1 - 6, "Sumbu X (m) →", fontsize=7.0, fontweight='bold', color='#1d4ed8', ha='center', va='bottom')
ax.text(170 - 8, out_y1 + 10, "Sumbu Y\n(m) ↓", fontsize=7.0, fontweight='bold', color='#1d4ed8', ha='right', va='top')

# 3. Survey Points Overlay (all 44 points)
for _, r in df_pts.iterrows():
    pid = r['titik_id']
    xpx = int(r['x_px'])
    ypx = int(r['y_px'])
    num_str = pid.split('-')[-1]
    if pid == 'L4-000':
        ax.plot(xpx, ypx, marker='o', markersize=8.5, color='#dc2626',
                markeredgecolor='white', markeredgewidth=1.2, zorder=20)
        ax.text(xpx + 8, ypx - 5, 'CAL (00)', fontsize=7.5, fontweight='heavy',
                color='#dc2626', path_effects=halo_cal, zorder=21)
    elif int(num_str) >= 34:
        # Sayap Barat
        ax.plot(xpx, ypx, marker='o', markersize=6.2, color='#059669',
                markeredgecolor='white', markeredgewidth=0.9, zorder=15)
        ax.text(xpx + 6, ypx - 4, f'{int(num_str)}', fontsize=7.5, fontweight='bold',
                color='#065f46', path_effects=halo_point, zorder=16)
    else:
        # Bangunan Inti
        ax.plot(xpx, ypx, marker='o', markersize=5.5, color='#1d4ed8',
                markeredgecolor='white', markeredgewidth=0.8, zorder=15)
        ax.text(xpx + 5, ypx - 4, f'{int(num_str)}', fontsize=7.0, fontweight='bold',
                color='#0f172a', path_effects=halo_point, zorder=16)

# 4. North Arrow
nx, ny = 90, 140
ax.annotate('', xy=(nx, ny - 28), xytext=(nx, ny + 12),
            arrowprops=dict(facecolor='#0f172a', edgecolor='none', width=2.5, headwidth=9, headlength=11), zorder=10)
ax.text(nx, ny - 35, "U", fontsize=9, fontweight='heavy', color='#0f172a', ha='center', va='bottom', zorder=11)

# 5. Scale Bar
sb_x, sb_y = 1280, 890
bar_len_5m = int(round(5 * SCALE_M))  # ~ 113 px
ax.plot([sb_x, sb_x + bar_len_5m], [sb_y, sb_y], color='#0f172a', linewidth=2.0, zorder=10)
ax.plot([sb_x, sb_x], [sb_y - 4, sb_y + 4], color='#0f172a', linewidth=1.2, zorder=10)
ax.plot([sb_x + bar_len_5m / 2, sb_x + bar_len_5m / 2], [sb_y - 3, sb_y + 3], color='#0f172a', linewidth=0.8, zorder=10)
ax.plot([sb_x + bar_len_5m, sb_x + bar_len_5m], [sb_y - 4, sb_y + 4], color='#0f172a', linewidth=1.2, zorder=10)
ax.text(sb_x, sb_y - 7, "0", fontsize=6.5, ha='center', color='#0f172a', zorder=11)
ax.text(sb_x + bar_len_5m / 2, sb_y - 7, "2.5m", fontsize=6.5, ha='center', color='#0f172a', zorder=11)
ax.text(sb_x + bar_len_5m, sb_y - 7, "5m", fontsize=6.5, ha='center', color='#0f172a', zorder=11)
ax.text(sb_x + bar_len_5m / 2, sb_y + 9, f"SKALA ({SCALE_M:.1f} px/m)", fontsize=6.5, fontweight='bold', ha='center', color='#475569', zorder=11)

# Legend
legend_text = '● Biru: Titik Inti Gedung (01–33)   │   ● Hijau: Titik Sayap Barat (34–43)'
ax.text(W / 2, 1010, legend_text, fontsize=8.2, fontweight='bold', ha='center', va='center',
        color='#334155', zorder=25,
        bbox=dict(boxstyle='round,pad=0.3', fc='#f8fafc', ec='#cbd5e1', lw=0.8))

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
sketsa_out_path = os.path.join(DENAH_DIR, 'denah_sketsa_kartesius.png')
plt.savefig(sketsa_out_path, dpi=100)
plt.close(fig)
print(f"[OK] {sketsa_out_path} berhasil dibuat.")
