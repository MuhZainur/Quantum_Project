# 🚀 CARA DEPLOY KE HUGGINGFACE (SUPER MUDAH!)

## Langkah Cepat (3 Menit):

### 1️⃣ Buat Space di HuggingFace
- Buka: https://huggingface.co/new-space
- **Owner:** Zainajabroh
- **Space name:** `retail-analytics-api`
- **License:** MIT
- **Select SDK:** Docker
- **Space hardware:** CPU basic (Free!)
- Klik **"Create Space"**

### 2️⃣ Dapatkan Token
- Buka: https://huggingface.co/settings/tokens
- Klik **"New token"**
- **Name:** `retail-deploy`
- **Type:** Write
- Klik **"Generate"**
- **COPY TOKEN** (Anda akan butuh ini sebentar lagi!)

### 3️⃣ Jalankan Script Otomatis
- Double-click file: `deploy_to_hf.bat`
- Paste token Anda ketika diminta
- Ketik `y` dan Enter
- Tunggu selesai (~2 menit upload)

### 4️⃣ Cek Hasil
Buka: https://huggingface.co/spaces/Zainajabroh/retail-analytics-api

Tunggu ~10 menit untuk build. Jika berhasil, status akan hijau "Running".

API URL Anda: `https://zainajabroh-retail-analytics-api.hf.space`

---

## ❓ Troubleshooting
- **"Error: Space not found"** → Pastikan Anda sudah create Space di langkah 1
- **"Build failed"** → Cek tab "Logs" di HF Space untuk detail error
- **"CORS error di Frontend"** → Normal, nanti fix setelah connect Vercel

DONE! 🎉
