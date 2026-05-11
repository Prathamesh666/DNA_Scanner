#!/bin/bash
# Ezerhost VPS Deployment Script for Flask + DeepFace (DNA_Scanner repo)
# Beginner-proof version with venv creation + non-root user

APP_DIR=/root/DNA_Scanner
APP_MODULE=main:app
DEPLOY_USER=www-data   # safer than root

# Update system
sudo apt update && sudo apt upgrade -y

# Install essentials
sudo apt install -y python3 python3-pip python3-venv git nginx certbot python3-certbot-nginx

# Clone repo if not present
if [ ! -d "$APP_DIR" ]; then
    sudo git clone https://github.com/Prathamesh666/DNA_Scanner.git $APP_DIR
fi

# Create virtual environment if not exists
if [ ! -d "$APP_DIR/venv" ]; then
    sudo python3 -m venv $APP_DIR/venv
fi

# Activate venv and install dependencies
source $APP_DIR/venv/bin/activate
pip install --upgrade pip
pip install -r $APP_DIR/requirements.txt

# Create Gunicorn systemd service
SERVICE_FILE=/etc/systemd/system/gunicorn.service
sudo tee $SERVICE_FILE > /dev/null <<EOL
[Unit]
Description=Gunicorn instance for DNA_Scanner Flask app
After=network.target

[Service]
User=$DEPLOY_USER
Group=$DEPLOY_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 1 --threads 8 --worker-class gthread --preload --timeout 180 --bind 127.0.0.1:8000 $APP_MODULE
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

# Enable and start Gunicorn
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl restart gunicorn

# Configure Nginx reverse proxy (HTTP -> HTTPS redirect)
NGINX_FILE=/etc/nginx/sites-available/dna-analyzer.conf
sudo tee $NGINX_FILE > /dev/null <<EOL
server {
    listen 80;
    server_name dna-analyzer.duckdns.org;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name dna-analyzer.duckdns.org;

    ssl_certificate /etc/letsencrypt/live/dna-analyzer.duckdns.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dna-analyzer.duckdns.org/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOL

# Enable Nginx site
sudo ln -sf $NGINX_FILE /etc/nginx/sites-enabled/dna-analyzer.conf
sudo nginx -t && sudo systemctl reload nginx

# Issue Let's Encrypt certificate (only first time)
sudo certbot --nginx -d dna-analyzer.duckdns.org --non-interactive --agree-tos -m your-email@example.com

echo "✅ Deployment complete. Your app is live at https://dna-analyzer.duckdns.org"

echo "Note: Used DuckDNS Website for free domain and SSL certificate. You can replace it with your own domain if you have one."