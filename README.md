# Dashboard Klasifikasi Data Pelanggan (ID3) — Mulana Property

Aplikasi **dashboard interaktif** berbasis **Streamlit** untuk visualisasi data pelanggan dan klasifikasi keputusan menggunakan algoritma **Decision Tree (ID3)**.  
Menyediakan filter data, ringkasan KPI, tampilan model ID3, dan fitur prediksi sederhana.

## Fitur
- Dashboard ringkasan KPI (Total Data, Keputusan Iya/Tidak, Persentase)
- Filter data pelanggan (mis. pekerjaan/kredit/keputusan — sesuai kolom di CSV)
- Visualisasi data (grafik ringkasan & distribusi)
- Model klasifikasi **ID3 (Decision Tree)** + insight sederhana
- Menu Prediksi (input fitur → hasil prediksi)

## Tech Stack
- Python
- Streamlit
- Pandas / NumPy
- Matplotlib / Plotly (jika dipakai)
- Scikit-learn (opsional, jika dipakai untuk bantu evaluasi)

## Screenshot
### 1) Dashboard / Visualisasi
<img width="1917" height="873" alt="Screenshot 2026-01-15 015358" src="https://github.com/user-attachments/assets/89461774-0cf8-4261-b3df-756a7ea5b195" />

### 2) Data (Setelah Difilter)
<img width="1904" height="863" alt="Screenshot 2026-01-15 133559" src="https://github.com/user-attachments/assets/4e16875e-ac76-4780-a788-cd93c764057d" />

### 3) Model ID3
<img width="1910" height="889" alt="Screenshot 2026-01-15 133647" src="https://github.com/user-attachments/assets/611bd73c-001d-4f6f-b674-52effc1b0c7f" />

### 4) Prediksi
<img width="1914" height="881" alt="Screenshot 2026-01-15 133736" src="https://github.com/user-attachments/assets/723e762a-bb4b-41c1-80a1-ae2786dea899" />

## Cara Menjalankan (Local)
1. Clone
```bash
git clone https://github.com/Mulana362/Klasifikasi-Data-Pelanggan.git
cd Klasifikasi-Data-Pelanggan
```
2. Jalankan Streamlit
```bash
streamlit run app.py
```
3. Buka di browser
```text
http://localhost:8501
```
