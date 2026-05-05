#!/bin/bash
set -e

echo "🔄 Pulling latest code..."
cd /root/DNA_Scanner
git pull origin main

echo "📦 Restarting Gunicorn service..."
sudo systemctl restart gunicorn

echo "🌐 Reloading Nginx..."
sudo systemctl reload nginx

echo "✅ Deployment complete. Showing Gunicorn logs..."
sudo systemctl status gunicorn --no-pager
