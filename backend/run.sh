#!/bin/bash
# Unix/Linux/Mac startup script for the development server

cd "$(dirname "$0")" || exit 1

echo "Starting Deepfake Video Detection API..."
python run.py --reload
