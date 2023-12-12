#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static

# Update packages and install Nginx if not already installed
sudo apt-get -y update
sudo apt-get -y install nginx

# Configure firewall to allow Nginx if not already done
sudo ufw allow 'Nginx HTTP'

# Create directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create dummy HTML to test Nginx configuration
echo -e "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>" > index.html
sudo mv index.html /data/web_static/releases/test/

# Create symbolic link to test folder
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data folder to ubuntu user and group
sudo chown -hR ubuntu:ubuntu /data/

# Modify Nginx to serve /data/web_static_current at /hbnb_static
loc_str="server_name _;\n\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}"
sudo sed -i "s/server_name _;/$loc_str/" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
