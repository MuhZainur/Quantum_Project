# Panduan Deployment Cloud (Aman & Gratis) 🚀

Panduan ini akan membantu Anda meng-online-kan project Retail Analytics Anda ke layanan Cloud (Render atau Railway) tanpa membocorkan data sensitif.

---

## 🔒 1. Mekanisme Keamanan (Otomatis)
Saya telah membuat file `.gitignore` yang sangat ketat di folder project Anda.
**Efeknya:**
*   Saat Anda upload ke GitHub, file `QVI_data.csv`, `*.xlsx`, dan data log customer **TIDAK AKAN** ikut ter-upload.
*   Yang ter-upload hanya: Script Python, Website React, dan Model `.pkl`.
*   **Aman:** Dataset perusahaan tetap di laptop Anda.

---

## 🛠️ 2. Persiapan GitHub
1.  Buka [GitHub](https://github.com/new) dan buat repository baru (Misal: `quantum-retail-ai`).
2.  Buka terminal di folder project Anda (`H:\coding\Quantum_Virtual_Project\`) dan jalankan:

```bash
git init
git add .
git commit -m "First commit - Retail AI App"
git branch -M main
git remote add origin https://github.com/MuhZainur/quantum-retail-ai.git
git push -u origin main
```

---

## ☁️ 3. Deploy ke Render (Opsi Paling Mudah)
Kita akan men-deploy Backend dan Frontend secara terpisah.

### A. Deploy Backend (API)
1.  Daftar di [dashboard.render.com](https://dashboard.render.com).
2.  Klik **New +** -> **Web Service**.
3.  Connect repository GitHub Anda.
4.  isi setting berikut:
    *   **Name:** `retail-api`
    *   **Root Directory:** `MLE/Backend`  <-- *PENTING!*
    *   **Environment:** `Python 3`
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`
5.  Klik **Deploy**. Tunggu sampai hijau (Live).
6.  Copy URL API Anda (misal: `https://retail-api.onrender.com`).

### B. Deploy Frontend (Dashboard)
1.  Di Render, buat **New +** -> **Static Site**.
2.  Connect repository yang sama.
3.  Isi setting:
    *   **Name:** `retail-dashboard`
    *   **Root Directory:** `MLE/Frontend` <-- *PENTING!*
    *   **Build Command:** `npm install && npm run build`
    *   **Publish Directory:** `dist`
4.  **Setting Wajib:** Masukkan URL API.
    *   Pergi ke menu "Environment Variables".
    *   Key: `VITE_API_BASE_URL`
    *   Value: `https://retail-api.onrender.com` (URL dari langkah A)
5.  Klik **Deploy**.

---

## ❓ FAQ

**Q: Kalau data tidak di-upload, apakah Data Drift Monitoring jalan?**
A: Di versi live ini, fitur `/monitoring/churn/drift` mungkin akan error karena file `reference_churn_data.csv` tidak ada di server.
*   *Solusi:* Jika Anda mau fitur ini jalan, Anda harus meng-upload file `MLE/Backend/reference_churn_data.csv` secara manual (Uncomment baris di `.gitignore`). File ini aman karena isinya cuma angka agregat (Recency, Frequency), tidak ada nama/ID customer.

**Q: Apakah modelnya jalan tanpa data asli?**
A: **Jalan 100%.** Model `.pkl` sudah "belajar" dari data. Dia tidak butuh data asli lagi untuk melakukan prediksi masa depan.
