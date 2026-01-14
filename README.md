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
<img width="1904" height="923" alt="Dashboard / Visualisasi" src="https://github.com/user-attachments/assets/3274cf00-b6b1-4824-8706-441f311a60a5" />

### 2) Data (Setelah Difilter)
<img width="1904" height="872" alt="Data (Setelah Difilter)" src="https://github.com/user-attachments/assets/14c50254-1214-486a-af7a-4b7a445b36e4" />

### 3) Model ID3
<img width="1907" height="866" alt="Model ID3" src="https://github.com/user-attachments/assets/e41c5269-bb05-41ff-9e83-500ac7642b49" />

### 4) Prediksi
<img width="1911" height="884" alt="Prediksi" src="https://github.com/user-attachments/assets/95f25668-7846-471e-9997-522172d5cce7" />

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
