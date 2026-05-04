#!/bin/bash
# Hostinger VPS Deployment Script for Flask + DeepFace (DNA_Scanner repo)

APP_DIR=/root/DNA_Scanner        # repo path after cloning
APP_MODULE=main:app              # Flask entry point (main.py defines app)

# Update system
sudo apt update && sudo apt upgrade -y

# Install essentials
sudo apt install -y python3 python3-pip git nginx

# Clone your repo (skip if already uploaded)
if [ ! -d "$APP_DIR" ]; then
    git clone https://github.com/Prathamesh666/DNA_Scanner.git $APP_DIR
fi

# Install Python dependencies from requirements.txt
pip3 install -r $APP_DIR/requirements.txt

# Create Gunicorn systemd service
SERVICE_FILE=/etc/systemd/system/deepface.service
sudo tee $SERVICE_FILE > /dev/null <<EOL
[Unit]
Description=Gunicorn instance for DeepFace Flask app
After=network.target

[Service]
User=root
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/gunicorn -w 2 -b 127.0.0.1:5000 $APP_MODULE
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Enable and start service
sudo systemctl enable deepface
sudo systemctl start deepface

# Configure Nginx reverse proxy
NGINX_FILE=/etc/nginx/sites-available/deepface
sudo tee $NGINX_FILE > /dev/null <<EOL
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOL

# Enable Nginx site
sudo ln -s $NGINX_FILE /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

echo "✅ Deployment complete. Your app is live at http://<your-vps-ip>"
