#!/bin/bash
cd /root/DNA_Scanner
git pull origin main
sudo systemctl restart gunicorn
