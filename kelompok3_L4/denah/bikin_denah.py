import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
import pandas as pd
from PIL import Image

BASE_DIR = r'c:\Users\kuahs\Documents\Jarnik'
DENAH_DIR = os.path.join(BASE_DIR, 'kelompok3_L4', 'denah')
DATA_DIR = os.path.join(BASE_DIR, 'kelompok3_L4', 'data')
os.makedirs(DENAH_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Base clean image
clean_path = os.path.join(BASE_DIR, 'final_clean.png')
if not os.path.exists(clean_path):
    # Inpaint from final.jpeg
    src_final = os.path.join(BASE_DIR, 'final.jpeg')
    im = Image.open(src_final).convert('RGB')
    arr = np.array(im)
    from scipy.ndimage import binary_dilation
    red_mask = (arr[:, :, 0] > 150) & (arr[:, :, 1] < 80) & (arr[:, :, 2] < 80)
    red_mask_dilated = binary_dilation(red_mask, iterations=2)
    arr[red_mask_dilated] = [255, 255, 255]
    im_clean = Image.fromarray(arr)
    im_clean.save(clean_path)
else:
    im_clean = Image.open(clean_path).convert('RGB')

# Save clean denah for analyze.py
im_clean.save(os.path.join(DENAH_DIR, 'denah_L4.png'))

# 2. Points table
df_pts = pd.read_csv(os.path.join(BASE_DIR, 'titik_L4.csv'))
df_pts.to_csv(os.path.join(DATA_DIR, 'titik_L4.csv'), index=False)

# 3. Generate final_titik.png (dots + numbers only, no title, no legend)
fig, ax = plt.subplots(figsize=(16, 10.35), dpi=100)
ax.imshow(im_clean)
halo_point = [pe.withStroke(linewidth=2.4, foreground='white')]

for _, r in df_pts.iterrows():
    pid = r['titik_id']
    xpx = int(r['x_px'])
    ypx = int(r['y_px'])
    num_str = pid.split('-')[-1]
    
    if pid == 'L4-000':
        ax.plot(xpx, ypx, marker='o', markersize=8.0, color='#dc2626',
                markeredgecolor='white', markeredgewidth=1.2, zorder=20)
        ax.text(xpx + 7, ypx - 4, '00', fontsize=7.5, fontweight='heavy',
                color='#dc2626', path_effects=halo_point, zorder=21)
    elif int(num_str) >= 34:
        ax.plot(xpx, ypx, marker='o', markersize=6.0, color='#059669',
                markeredgecolor='white', markeredgewidth=0.9, zorder=15)
        ax.text(xpx + 6, ypx - 4, f'{int(num_str)}', fontsize=7.5, fontweight='bold',
                color='#065f46', path_effects=halo_point, zorder=16)
    else:
        ax.plot(xpx, ypx, marker='o', markersize=5.5, color='#1d4ed8',
                markeredgecolor='white', markeredgewidth=0.8, zorder=15)
        ax.text(xpx + 5, ypx - 4, f'{int(num_str)}', fontsize=7.0, fontweight='bold',
                color='#0f172a', path_effects=halo_point, zorder=16)

ax.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig(os.path.join(BASE_DIR, 'final_titik.png'), dpi=100)
plt.savefig(os.path.join(BASE_DIR, 'final_titik.jpeg'), dpi=100)
plt.savefig(os.path.join(DENAH_DIR, 'denah_titik_L4.png'), dpi=100)
plt.close(fig)

# 4. Generate final_titik_polos.png (dots only, no text at all)
fig, ax = plt.subplots(figsize=(16, 10.35), dpi=100)
ax.imshow(im_clean)

for _, r in df_pts.iterrows():
    pid = r['titik_id']
    xpx = int(r['x_px'])
    ypx = int(r['y_px'])
    num_str = pid.split('-')[-1]
    
    if pid == 'L4-000':
        ax.plot(xpx, ypx, marker='o', markersize=9.0, color='#dc2626',
                markeredgecolor='white', markeredgewidth=1.2, zorder=20)
    elif int(num_str) >= 34:
        ax.plot(xpx, ypx, marker='o', markersize=6.5, color='#059669',
                markeredgecolor='white', markeredgewidth=0.9, zorder=15)
    else:
        ax.plot(xpx, ypx, marker='o', markersize=6.0, color='#1d4ed8',
                markeredgecolor='white', markeredgewidth=0.8, zorder=15)

ax.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig(os.path.join(BASE_DIR, 'final_titik_polos.png'), dpi=100)
plt.savefig(os.path.join(BASE_DIR, 'final_titik_polos.jpeg'), dpi=100)
plt.savefig(os.path.join(DENAH_DIR, 'denah_titik_polos.png'), dpi=100)
plt.close(fig)

print("[OK] Berhasil generate final_titik.png dan final_titik_polos.png")
