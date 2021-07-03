#!/bin/bash
sudo apt install python3 pip python3.8-venv python3-flask gunicorn
curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python -
pdm --pep582 >> ~/.bash_profile
sudo ufw allow 5000
