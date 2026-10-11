import os, sys, shutil
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

data_dir = r'c:\Users\kuahs\Documents\Jarnik\kelompok3_L4\data'
raw_dir = os.path.join(data_dir, 'raw_downloaded')
batch_dir = os.path.join(raw_dir, 'fresh_batch')
titik_csv_path = r'c:\Users\kuahs\Documents\Jarnik\titik_L4.csv'

# Load reference titik
ref_titik = pd.read_csv(titik_csv_path)
titik_map = {}
for _, row in ref_titik.iterrows():
    titik_map[str(row['titik_id']).strip()] = (row['x_px'], row['y_px'], str(row['keterangan']).strip())

# Clean mapping of all members and retakes to latest source files
pembagian = [
    # 1. Dave: passive & active lengkap (L4-001, L4-034, L4-038, L4-041; active: L4-001..003, 034, 038, 041)
    (1, "Dave", "A", 
     [os.path.join(data_dir, "passive_L4_01_Dave.csv")], 
     [os.path.join(data_dir, "active_L4_01_Dave.csv")]),
     
    # 2. Jason: passive & active lengkap (L4-004, 005, 006, 035, 039, 042)
    (2, "Jason", "B", 
     [os.path.join(data_dir, "passive_L4_02_Jason.csv")], 
     [os.path.join(data_dir, "active_L4_02_Jason.csv")]),
     
    # 3. Hisyam: passive C; active C
    (3, "Hisyam", "C", 
     [os.path.join(batch_dir, "passive_L4_C.csv")], 
     [os.path.join(batch_dir, "active_L4_C.csv")]),
     
    # 4. Tobias: passive D; active D (L4-010, 011, 012, 029)
    (4, "Tobias", "D", 
     [os.path.join(data_dir, "passive_L4_D.csv")], 
     [os.path.join(data_dir, "active_L4_04_Tobias.csv")]),
     
    # 5. Willy: passive E; active E
    (5, "Willy", "E", 
     [os.path.join(batch_dir, "passive_L4_E.csv")], 
     [os.path.join(batch_dir, "active_L4_E.csv")]),
     
    # 6. Edgar: passive F; active F
    (6, "Edgar", "F", 
     [os.path.join(batch_dir, "passive_L4_F.csv")], 
     [os.path.join(raw_dir, "active_L4.csv")]),
     
    # 7. Joshua: passive & active lengkap (L4-019..022, 036, 040, 043)
    (7, "Joshua", "G", 
     [os.path.join(data_dir, "passive_L4_07_Joshua.csv")], 
     [os.path.join(data_dir, "active_L4_07_Joshua.csv")]),
     
    # 8. Nada: passive H
    (8, "Nada", "H", 
     [os.path.join(batch_dir, "passive_L4_H.csv")], 
     [os.path.join(data_dir, "active_L4_08_Nada.csv")]),
     
    # 9. Saskia: passive I; active I
    (9, "Saskia", "I", 
     [os.path.join(batch_dir, "passive_L4_I.csv")], 
     [os.path.join(batch_dir, "active_L4_I.csv")]),
     
    # 10. Charisa: passive J
    (10, "Charisa", "J", 
     [os.path.join(batch_dir, "passive_L4_J.csv")], 
     None),
     
    # 11. Raisya: passive K
    (11, "Raisya", "K", 
     [os.path.join(batch_dir, "passive_L4_K.csv")], 
     None),

    # 12. Retake Khusus Perimeter Luar (Outdoor: L4-008 & L4-025)
    (12, "Retake_Outdoor", "Perimeter",
     None,
     [os.path.join(batch_dir, "active_L4_A3.csv")]),
]

all_passive_dfs = []
all_active_dfs = []
summary = []

for item in pembagian:
    num, name, block, pass_sources, act_sources = item
    pass_dst = os.path.join(data_dir, f"passive_L4_{num:02d}_{name}.csv")
    act_dst = os.path.join(data_dir, f"active_L4_{num:02d}_{name}.csv")
    
    pass_rows = 0
    titik_list = []
    
    # Process Passive
    if pass_sources:
        pass_dfs = []
        for psrc in pass_sources:
            if os.path.exists(psrc):
                df_p = pd.read_csv(psrc)
                pass_dfs.append(df_p)
            elif os.path.exists(os.path.join(raw_dir, os.path.basename(psrc))):
                df_p = pd.read_csv(os.path.join(raw_dir, os.path.basename(psrc)))
                pass_dfs.append(df_p)
        
        if pass_dfs:
            combined_member_pass = pd.concat(pass_dfs, ignore_index=True)
            combined_member_pass['anggota'] = name
            combined_member_pass['blok'] = block
            
            # Fill missing coordinates
            for idx, r in combined_member_pass.iterrows():
                tid = str(r.get('titik_id', '')).strip()
                if tid in titik_map:
                    if pd.isna(r.get('x_px')) or r.get('x_px') == '':
                        combined_member_pass.at[idx, 'x_px'] = titik_map[tid][0]
                    if pd.isna(r.get('y_px')) or r.get('y_px') == '':
                        combined_member_pass.at[idx, 'y_px'] = titik_map[tid][1]
            
            # Remove duplicates if any
            combined_member_pass.to_csv(pass_dst, index=False)
            all_passive_dfs.append(combined_member_pass)
            pass_rows = len(combined_member_pass)
            titik_list = sorted(combined_member_pass['titik_id'].dropna().unique().tolist())
            
    # Process Active
    act_rows = 0
    if act_sources:
        act_dfs = []
        for asrc in act_sources:
            if os.path.exists(asrc):
                df_a = pd.read_csv(asrc)
                act_dfs.append(df_a)
            elif os.path.exists(os.path.join(raw_dir, os.path.basename(asrc))):
                df_a = pd.read_csv(os.path.join(raw_dir, os.path.basename(asrc)))
                act_dfs.append(df_a)
                
        if act_dfs:
            combined_member_act = pd.concat(act_dfs, ignore_index=True)
            combined_member_act['anggota'] = name
            combined_member_act['blok'] = block
            combined_member_act.to_csv(act_dst, index=False)
            all_active_dfs.append(combined_member_act)
            act_rows = len(combined_member_act)
            if not titik_list:
                titik_list = sorted(combined_member_act['titik_id'].dropna().unique().tolist())
                
    summary.append({
        "No": num,
        "Nama": name,
        "Blok": block,
        "Titik_Ukur": ", ".join(titik_list) if titik_list else "-",
        "File_Passive": f"passive_L4_{num:02d}_{name}.csv" if pass_rows > 0 else "-",
        "Baris_Passive": pass_rows,
        "File_Active": f"active_L4_{num:02d}_{name}.csv" if act_rows > 0 else "-",
        "Baris_Active": act_rows
    })

# Master Combined Passive
if all_passive_dfs:
    combined_pass = pd.concat(all_passive_dfs, ignore_index=True)
    pass_gabungan = os.path.join(data_dir, "passive_L4_gabungan.csv")
    pass_master = os.path.join(data_dir, "passive_L4.csv")
    combined_pass.to_csv(pass_gabungan, index=False)
    combined_pass.to_csv(pass_master, index=False)
    print(f"\n[PASSIVE] Berhasil menggabungkan {len(combined_pass)} baris ke:")
    print(f" - {pass_gabungan}")
    print(f" - {pass_master}")

# Master Combined Active
if all_active_dfs:
    combined_act = pd.concat(all_active_dfs, ignore_index=True)
    # Deduplicate active scan by titik_id, keeping the latest timestamp
    combined_act['ts_sort'] = pd.to_datetime(combined_act['timestamp'], errors='coerce')
    combined_act = combined_act.sort_values('ts_sort').drop_duplicates(subset=['titik_id'], keep='last').drop(columns=['ts_sort'])
    
    act_cols = ["timestamp", "titik_id", "bssid_assoc", "freq_mhz", "rssi_dbm", "tx_rate_mbps",
                "rtt_avg_ms", "rtt_max_ms", "jitter_ms", "loss_pct", "down_mbps", "up_mbps", "metode_rtt", "anggota", "blok"]
    for c in act_cols:
        if c not in combined_act.columns:
            combined_act[c] = None
    combined_act = combined_act[act_cols]
    
    act_gabungan = os.path.join(data_dir, "active_L4_gabungan.csv")
    act_master = os.path.join(data_dir, "active_L4.csv")
    combined_act.to_csv(act_gabungan, index=False)
    combined_act.to_csv(act_master, index=False)
    print(f"\n[ACTIVE] Berhasil menggabungkan {len(combined_act)} titik aktif unik ke:")
    print(f" - {act_gabungan}")
    print(f" - {act_master}")

# Copy Roaming Log
roam_src = os.path.join(batch_dir, 'passive_L4_G_1.csv')
if os.path.exists(roam_src):
    roam_dst = os.path.join(data_dir, 'roaming_L4.csv')
    shutil.copy2(roam_src, roam_dst)
    print(f"\n[ROAMING] Berhasil memperbarui log roaming ke: {roam_dst}")

sum_df = pd.DataFrame(summary)
print("\n" + "="*85)
print("REKAP PEMETAAN DATASET TERBARU LANTAI 4 KELOMPOK 3")
print("="*85)
print(sum_df.to_string(index=False))
print("="*85)
