#!/bin/bash
set -euxo pipefail
apt-get update -y
apt-get install -y docker.io git
systemctl enable --now docker
usermod -aG docker ubuntu || true
cd /home/ubuntu
if [ ! -d repo ]; then
  git clone https://github.com/YOUR_ORG/croody.git repo
fi
cd repo
cp proyecto_integrado/.env.example proyecto_integrado/.env || true
chmod +x deploy_from_scratch.sh
./deploy_from_scratch.sh
