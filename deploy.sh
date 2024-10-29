#!/bin/bash
set -e  # Exit on error

echo "Starting deployment process..."
echo "Publishing package using setup.py..."

python3 setup.py publish

echo "✅ Deployment completed successfully!"