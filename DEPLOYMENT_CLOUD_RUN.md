# Quantum Retail Analytics - Deployment Guide

## 🚀 Deploy to Google Cloud Run

This guide will help you deploy the Quantum Retail Analytics application (Backend + Frontend) to Google Cloud Platform.

---

## Prerequisites

1. **GCP Account** with billing enabled
2. **gcloud CLI** installed ([Install Guide](https://cloud.google.com/sdk/docs/install))
3. **Docker** installed locally (optional, for local testing)

---

## 🔧 Initial Setup

### 1. Login and Set Project

```bash
# Login to GCP
gcloud auth login

# Set your project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### 2. Create Artifact Registry Repository (Recommended)

```bash
# Create repository in Asia Southeast region
gcloud artifacts repositories create quantum-retail \
  --repository-format=docker \
  --location=asia-southeast2 \
  --description="Quantum Retail Analytics Docker images"

# Configure Docker to authenticate with Artifact Registry
gcloud auth configure-docker asia-southeast2-docker.pkg.dev
```

---

## 📦 Deploy Backend (FastAPI)

### Step 1: Build and Push Docker Image

```bash
cd MLE/Backend

# Build image
gcloud builds submit \
  --tag asia-southeast2-docker.pkg.dev/$PROJECT_ID/quantum-retail/backend:latest
```

### Step 2: Deploy to Cloud Run

```bash
gcloud run deploy quantum-backend \
  --image asia-southeast2-docker.pkg.dev/$PROJECT_ID/quantum-retail/backend:latest \
  --platform managed \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars ALLOWED_ORIGINS="*"
```

**Note:** After deployment, you'll get a URL like: `https://quantum-backend-xxxxx.a.run.app`

### Step 3: Test Backend

```bash
# Get the backend URL
export BACKEND_URL=$(gcloud run services describe quantum-backend \
  --region asia-southeast2 \
  --format 'value(status.url)')

# Test health endpoint
curl $BACKEND_URL/

# Test prediction (churn)
curl -X POST $BACKEND_URL/predict/churn \
  -H "Content-Type: application/json" \
  -d '{
    "recency": 10,
    "frequency": 5,
    "monetary": 25.50,
    "lifestage": "YOUNG SINGLES/COUPLES",
    "premium_customer": "Mainstream"
  }'
```

---

## 🎨 Deploy Frontend (React + Vite)

### Step 1: Update Frontend to Use Backend URL

Before building, configure the frontend to point to your deployed backend.

```bash
cd MLE/Frontend

# Create production environment file
cat > .env.production << EOF
VITE_API_URL=$BACKEND_URL
EOF
```

### Step 2: Build and Push Docker Image

```bash
cd MLE/Frontend

# Build image
gcloud builds submit \
  --tag asia-southeast2-docker.pkg.dev/$PROJECT_ID/quantum-retail/frontend:latest
```

### Step 3: Deploy to Cloud Run

```bash
gcloud run deploy quantum-frontend \
  --image asia-southeast2-docker.pkg.dev/$PROJECT_ID/quantum-retail/frontend:latest \
  --platform managed \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --set-env-vars VITE_API_URL=$BACKEND_URL
```

---

## 💰 Cost Optimization

**Set minimum instances to 0 (scale to zero when idle)**

```bash
gcloud run services update quantum-backend \
  --region asia-southeast2 \
  --min-instances 0 --max-instances 5
```

**Estimated Cost:** ~$0-5/month for light usage

---

## 🎯 Quick Deploy Script

Save as `deploy.sh` in MLE folder:

```bash
#!/bin/bash
set -e

PROJECT_ID="your-project-id"
REGION="asia-southeast2"

echo "🚀 Deploying Backend..."
cd Backend
gcloud builds submit --tag asia-southeast2-docker.pkg.dev/$PROJECT_ID/quantum-retail/backend:latest
gcloud run deploy quantum-backend \
  --image asia-southeast2-docker.pkg.dev/$PROJECT_ID/quantum-retail/backend:latest \
  --region $REGION --allow-unauthenticated

BACKEND_URL=$(gcloud run services describe quantum-backend --region $REGION --format 'value(status.url)')
echo "✅ Backend: $BACKEND_URL"

echo "🎨 Deploying Frontend..."
cd ../Frontend
gcloud builds submit --tag asia-southeast2-docker.pkg.dev/$PROJECT_ID/quantum-retail/frontend:latest
gcloud run deploy quantum-frontend \
  --image asia-southeast2-docker.pkg.dev/$PROJECT_ID/quantum-retail/frontend:latest \
  --region $REGION --allow-unauthenticated \
  --set-env-vars VITE_API_URL=$BACKEND_URL

FRONTEND_URL=$(gcloud run services describe quantum-frontend --region $REGION --format 'value(status.url)')
echo "✅ Frontend: $FRONTEND_URL"
echo "🎉 Done!"
```

Run: `chmod +x deploy.sh && ./deploy.sh`

---

## 📚 Resources

- [Cloud Run Docs](https://cloud.google.com/run/docs)
- [Pricing Calculator](https://cloud.google.com/products/calculator)
