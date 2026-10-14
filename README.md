# Deepfake Video Detection

A full-stack application for detecting manipulated videos. The repository contains a FastAPI backend for video processing and model inference, and a React/Vite frontend for interacting with the API.

## Project structure

- `backend/` — FastAPI application, model and inference code, training scripts, and setup documentation.
- `frontend/` — React application built with Vite.
- `backend/PROJECT_SETUP.md` — Backend setup and configuration guide.
- `backend/PROJECT_COMPLETION_SUMMARY.md` — Project implementation notes.

## Requirements

- Python 3.12 or newer
- Node.js and npm
- FFmpeg for video processing

## Run locally

### Backend

In a terminal, install the backend dependencies and start the API:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation is at `http://127.0.0.1:8000/docs`.

### Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local address printed by Vite. The frontend API client is configured for the backend at `http://127.0.0.1:8000/api/v1`.

## Data and model files

Datasets, uploaded videos, local databases, and trained model weights are intentionally excluded from Git. They can be large and may have separate access or redistribution terms. Obtain datasets from their original sources and train or provide model weights locally as needed.

## GitHub

Before publishing, review the files you plan to upload and ensure you have permission to share all code and assets. Do not commit `.env` files, credentials, private videos, datasets, databases, or trained weights.
