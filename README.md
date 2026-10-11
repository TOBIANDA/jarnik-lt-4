# Pemetaan Kualitas Sinyal Wi-Fi 5 GHz Lantai 4 Gedung F FILKOM
**Praktikum Jaringan Nirkabel CIF62217 — Kelompok 3 (Lantai 4)**

Proyek ini berisi data mentah site survey Wi-Fi 5 GHz, digitalisasi denah kartesius berskala, model propagasi gelombang mikro berbasis redaman material dinding (*Wall Attenuation Factor* / WAF), peta heatmap Ekahau-style, dokumen laporan akademik, serta salindia presentasi optimasi infrastruktur.

---

## 👥 Tim & Peran (Sesuai Modul Praktikum)
* **Juru Denah:** Tobias Andra Valentino (245150200111076)
* **Surveyor:** Dave Carnegie Ongsah (245150200111070)
* **Surveyor:** Joshua Nathanael Purba (245150201111001)
* **Anggota Tim Lainnya:**
  * Jason Manuel (245150201111050)
  * Muhammad Alif Hisyam (245150207111100)
  * Willy Gregory (245150200111089)
  * Edgar Jason Husin (245150201111047)
  * Qotratun Nada Salsabila (245150207111037)
  * Saskia Negita Faradiani (245150201111021)
  * Charisa Salsabila Larasati (245150201111022)
  * Raisya Nadiva (245150201111032)

---

## 📁 Struktur Direktori
```text
├── kelompok3_L4/
│   ├── data/                 # Dataset survei pasif dan aktif mentah & terintegrasi
│   ├── denah/                # Sketsa kartesius, grid kolom F6, denah berarsir
│   ├── output/               # L4_heatmap.png, L4_status.png, L4_titik.csv, L4_ap.csv
│   ├── laporan/              # Berkas DOCX, PDF laporan, dan PPTX presentasi
│   ├── generate_ekahau_heatmap.py   # Engine simulasi ray-tracing redaman dinding (WAF)
│   └── generate_clean_maps.py       # Generator peta status titik & posisi 6 AP fisik
├── titik_L4.csv              # Master koordinat piksel 43 titik ukur Lantai 4
├── Laporan_Praktikum_Survei_WiFi_Lantai4_Kelompok3.docx
├── Laporan_Praktikum_Survei_WiFi_Lantai4_Kelompok3.pdf
├── Optimasi Infrastruktur Wi-Fi X.pptx
└── README.md
```

---

## 📡 Ringkasan Temuan & Rekomendasi
1. **Sebaran Access Point Fisik:**
   * **Area Blok Tengah (2 AP):** AP Plafon R.4.4 (Kanal 40) dan AP Plafon R.4.3 (Kanal 161).
   * **Ruang Sayap Barat (4 AP):** AP Sayap 1 (Kanal 36), AP Sayap 3 (Kanal 48), AP Sayap 4 (Kanal 157 di L4-041), dan AP Sayap 6 (Kanal 153 di L4-043).
   * *Ruang Sayap 2 (L4-039) dan Ruang Sayap 5 (L4-042) bersih tanpa AP langsung.*
2. **Kualitas Layanan:**
   * 14 Titik Baik (32.6%)
   * 26 Titik Perhatian (60.5%)
   * 3 Titik Buruk (7.0%): L4-002 (Toilet - packet loss 25%), L4-012 (Teras luar - RSSI -70.2 dBm), L4-041 (Sayap 4 - CCI Kanal 157).
3. **Optimasi Nol Rupiah:**
   * Turunkan Tx Power AP lantai 2 & 3 sebesar 6 dB untuk mengeliminasi fenomena *floor bleed*.
   * Kunci lebar kanal pada 40 MHz terencana dan manfaatkan blok kanal UNII-2 DFS (kanal 52–64, 100–140).
