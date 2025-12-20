# Panduan Deploy ke HuggingFace & Vercel (100% Gratis!) 🚀

## 🎯 Arsitektur Deployment
- **Backend (API):** HuggingFace Spaces (Docker)
- **Frontend (Website):** Vercel

---

## 📋 Langkah 1: Deploy Backend ke HuggingFace Spaces

### A. Persiapan
1. Daftar di [hugging face.co](https://huggingface.co/join)
2. Buat Space baru:
   - Klik "New Space"
   - **Name:** `retail-analytics-api`
   - **SDK:** `Docker`
   - **Visibility:** Public
   - Klik "Create Space"

### B. Upload Code
1. Clone Space yang baru dibuat:
   ```bash
   git clone https://huggingface.co/spaces/MuhZainur/retail-analytics-api
   cd retail-analytics-api
   ```

2. Copy file Backend ke folder Space:
   ```bash
   # Dari folder project Anda
   cp -r H:\coding\Quantum_Virtual_Project\MLE\Backend/* .
   
   # Rename Dockerfile khusus HF
   mv Dockerfile.huggingface Dockerfile
   ```

3. Push ke HuggingFace:
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push
   ```

4. Tunggu build selesai (~10 menit). URL API Anda:
   ```
   https://muhzainur-retail-analytics-api.hf.space
   ```

---

## 🌐 Langkah 2: Deploy Frontend ke Vercel

### A. Persiapan
1. Daftar di [vercel.com](https://vercel.com/signup) (pakai GitHub)
2. Install Vercel CLI (opsional):
   ```bash
   npm install -g vercel
   ```

### B. Deploy via Web Dashboard (Paling Mudah)
1. Login ke Vercel Dashboard
2. Klik **"Add New Project"**
3. **Import Git Repository:**
   - Pilih `Quantum_Project` dari GitHub
   - **Root Directory:** `MLE/Frontend`
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

4. **Set Environment Variable:**
   - Klik "Environment Variables"
   - **Key:** `VITE_API_BASE_URL`
   - **Value:** `https://muhzainur-retail-analytics-api.hf.space` (URL HF Space Anda)
   - Klik "Add"

5. Klik **"Deploy"**

6. Setelah selesai, Anda akan dapat URL seperti:
   ```
   https://quantum-project-frontend.vercel.app
   ```

---

## ✅ Testing
Buka URL Frontend Vercel Anda, coba:
1. **Tab Sales Forecasting** - Input data dummy
2. **Tab Churn Prediction** - Input RFM metrics

Jika API error:
- Cek CORS di `main.py` (pastikan `allow_origins=["*"]`)
- Cek logs di HuggingFace Space

---

## 🔧 Update di Masa Depan
Jika Anda ubah kode:
- **Backend:** Push ke HuggingFace Space (auto redeploy)
- **Frontend:** Push ke GitHub main branch (Vercel auto redeploy)

Selamat! Aplikasi Anda sudah live dan bisa diakses siapa saja! 🎉
