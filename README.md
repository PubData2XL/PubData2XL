# PubData2XL
It is a web application built with Django in Python, designed to facilitate the downloading of PubMed data into Microsoft Excel spreadsheets and XML files.

# Requirements
PubData2XL is compatible with any system that supports Python, including Windows, Mac, and Linux platforms. At present, it operates on an AlmaLinux server equipped with 2GB of RAM, accommodating approximately 400 monthly visitors. You may adjust the server capacity based on your specific requirements, scaling either upwards or downwards as necessary.

# How to install PubData2XL?
The provided instructions are tailored for setting up PubData2XL on an AlmaLinux minimal server from DigitalOcean, which is the configuration we currently utilize. However, analogous procedures will be required to install PubData2XL on different platforms. It’s important to adapt the steps to fit the specific environment and system requirements of the platform you are using.

################################################################################
## AlmaLinux Basic Setup
################################################################################

### Update the server
```sudo dnf update -y && sudo dnf upgrade -y && sudo dnf clean all```
### Create an user with sudo access, sammy can be replaced by anything you like.
```
adduser sammy
passwd sammy
usermod -aG wheel sammy
```
### Install Nano editor and SELinux Policy Core Python Utilities
```sudo dnf -y install nano policycoreutils-python-utils```
### Optional security recommendation: Change the SSH port from the default port 22 to one of your choice.
```
sudo nano /etc/ssh/sshd_config
```
Remove the # to activate the following configurations.
```
port 5555
PermitRootLogin no
PasswordAuthentication yes
```
```sudo semanage port -a -t ssh_port_t -p tcp 5555```
### Install Firewall and open ports for http, https and ssh
```
sudo dnf install -y firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-port=5555/tcp
sudo firewall-cmd --permanent --remove-service=ssh
sudo firewall-cmd --reload
sudo systemctl restart sshd
```
### Reboot the server and reconnect via SSH using either port 22 or the port you chosed above.
```sudo reboot```
### Create the directories for the application and where the CSS, JS, Images, etc. will be served from.
```
sudo mkdir /home/sammy/webapps
sudo mkdir /home/sammy/webapps/pubdata2xl/
sudo mkdir /home/sammy/webapps/pubdata2xl/media
sudo mkdir /home/sammy/webapps/pubdata2xl/static
```
### Create empty index files. This is a security measure don't skip.
```
sudo touch /home/sammy/webapps/pubdata2xl/media/index.html
sudo touch /home/sammy/webapps/pubdata2xl/static/index.html
```
################################################################################
## Install NGINX Web Server
################################################################################
```
sudo dnf install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
```
### Make a copy of the default NGINX configuration file. If something goes wrong you can always restore this file.
```sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx_original.conf```
### Remove or comment (#) the server lines starting at server { ... and ending in ... }
```sudo nano /etc/nginx/nginx.conf```
### Create and apply the web server configuration lines.
```sudo nano /etc/nginx/conf.d/pubdata2xl.conf```
```
server {
	listen 80;
        listen [::]:80; # use only if IPv6 is available.
        #server_name _; # use this if running in localhost. e.g. virtual box.
        server_name www.pubdata2xl.com pubdata2xl.com; # if domain is available use this instead.
        
        location /static {
            alias /home/sammy/webapps/pubdata2xl/static;
            expires max;
        }

        location /media {
            alias /home/sammy/webapps/pubdata2xl/media;
            expires max;
        }
        location / {
            proxy_pass http://127.0.0.1:8080/; #Important: This ip:port must match Gunicorn port.
            proxy_pass_header Server;
            proxy_set_header Host $host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_connect_timeout 1800;
            proxy_send_timeout 1800;
            proxy_read_timeout 1800;
            send_timeout 1800;
        }
        server_tokens off;
        add_header Strict-Transport-Security "max-age=63072000; includeSubdomains; preload";
        add_header Access-Control-Allow-Origin https://$host;
        add_header Access-Control-Allow-Methods "GET, POST";
        add_header X-Permitted-Cross-Domain-Policies none;
        #deprecated add_header Expect-CT 'max-age=60, report-uri="https://$host/report"';
        add_header "X-XSS-Protection" "1; mode=block";
        add_header Referrer-Policy "same-origin";
        add_header Feature-Policy "geolocation 'none'; camera 'none';
                                   fullscreen 'none'; payment 'none';
                                   midi 'none'; sync-xhr 'none';";
        add_header Content-Security-Policy "default-src 'none'; manifest-src 'self'; script-src 'self';
                                            style-src 'self'; img-src 'self' data:; connect-src 'self';
                                            font-src 'self'; object-src 'none'; media-src 'self';
                                            form-action 'self'; frame-ancestors 'self'; base-uri 'none';";
        add_header X-Frame-Options SAMEORIGIN;
        add_header X-Content-Type-Options nosniff always;
}
```
### Test if NGINX was configured correctly
```sudo nginx -t```
### Reload NGINX
```sudo systemctl reload nginx```

################################################################################
## Install and Configure Python, PIP, Gunicorn, Django
################################################################################
```
sudo dnf install python3.11 -y
cd /home/sammy/webapps/pubdata2xl
sudo python3.11 -m venv .venv
source .venv/bin/activate
sudo chown -R $USER /home/sammy/webapps/pubdata2xl
pip install --upgrade pip gunicorn django
```
################################################################################
## Install and Configure PubData2XL
################################################################################
```
sudo dnf install wget unzip -y
cd /home/sammy/webapps/pubdata2xl
sudo wget https://github.com/PubData2XL/PubData2XL/archive/refs/heads/main.zip
sudo unzip main.zip
sudo mv PubData2XL-main/* .
sudo rm -rf main.zip PubData2XL-main/
pip install -r src/requirements.txt
sudo mkdir /home/sammy/webapps/pubdata2xl/src/apps/pubdata2xl/temp/
```
### Create .env file. Keep this file secure and private.
```
cd /home/sammy/webapps/pubdata2xl/src
sudo nano .env
```
```
SECRET_KEY = "JUST_TYPE_A_LONG_RANDOM_LINE_OF_CHARACTERS_THIS_IS_A_SECURITY_FEATURE_DO_NOT_SHARE_THIS_WITH_ANYONE_ALL_THIS_CAN_BE_USED_azAZ123456789@#$%^&*()?><~"
NCBI_API_KEY = "YOUR_OWN_NCBIAPI_KEY"
```
### Create a Systemd file to manage Gunicorn.
The ip:port in the --bind configurations must match the port set in NGINX configuration file.

```sudo nano /etc/systemd/system/pubdata2xl.service```
```
[Unit]
Description=PubData2XL daemon
After=network.target

[Service]
User=sammy
Group=nginx
WorkingDirectory=/home/sammy/webapps/pubdata2xl/src
Environment="PATH=/home/sammy/webapps/pubdata2xl/.venv/bin"
ExecStart=/home/sammy/webapps/pubdata2xl/.venv/bin/gunicorn \
          --preload \
          --timeout 1800 \
          --workers=4 \
          --threads=4 \
	  --worker-class="sync" \
          --worker-connections=1000 \
          --error-logfile /home/sammy/webapps/pubdata2xl/src/config/error.log \
          --access-logfile /home/sammy/webapps/pubdata2xl/src/config/access.log \
          --bind 127.0.0.1:8080 config.wsgi:application

[Install]
WantedBy=multi-user.target
```
### Adjust the directories permissions
```
sudo usermod -a -G sammy nginx
sudo chown -R sammy:nginx /home
sudo chmod 755 -R /home

sudo semanage fcontext -a -t httpd_sys_content_t "/home/sammy/webapps/pubdata2xl/static(/.*)?"
sudo restorecon -R -v /home/sammy/webapps/pubdata2xl/static
sudo semanage fcontext -a -t httpd_sys_content_t "/home/sammy/webapps/pubdata2xl/media(/.*)?"
sudo restorecon -R -v /home/sammy/webapps/pubdata2xl/media

sudo chcon -R -t bin_t /home/sammy/webapps/pubdata2xl/.venv/bin
sudo chown -R sammy:nginx /home/sammy/webapps/pubdata2xl
sudo systemctl daemon-reload
sudo systemctl enable pubdata2xl
sudo systemctl restart pubdata2xl && sudo systemctl restart nginx
sudo systemctl status pubdata2xl
```
################################################################################
## Configure letsencrypt.org certificates.
################################################################################

This allows the site to be served securely from https. Not needed if running locally. This requires owning a domain name.
```
sudo dnf install epel-release -y
sudo dnf install certbot python3-certbot-nginx -y

sudo certbot --nginx -d www.pubdata2xl.com -d pubdata2xl.com

sudo firewall-cmd --permanent --remove-service=http
sudo firewall-cmd --reload
```
################################################################################
## Create Cronjob to restart gunicorn service if down.
################################################################################

```sudo nano /home/sammy/webapps/pubdata2xl/src/config/restart_gunicorn_if_not_alive.sh```
```
#!/bin/bash

SERVICENAME="pubdata2xl"

systemctl is-active --quiet $SERVICENAME
STATUS=$? # returned value is active if running

if [[ "$STATUS" -ne "active" ]]; then
        echo "Service '$SERVICENAME' is not curently running... Starting now..."
        sudo service $SERVICENAME start
fi
```
## Make the file executable

```sudo chmod +x /home/sammy/webapps/pubdata2xl/src/config/restart_gunicorn_if_not_alive.sh```
## Install cronjob
```
sudo dnf install crontabs cronie cronie-anacron -y
sudo systemctl start crond && sudo systemctl enable crond
sudo systemctl status crond
```
## Add a cronjob
```sudo EDITOR=nano crontab -e```
```
* * * * * /home/sammy/webapps/pubdata2xl/src/config/restart_gunicorn_if_not_alive.sh
```

################################################################################
# Periodically update PubData2XL to the newest version.
################################################################################
```
cd /home/sammy/webapps/pubdata2xl
source /home/sammy/webapps/pubdata2xl/.venv/bin/activate
sudo wget https://github.com/PubData2XL/PubData2XL/archive/refs/heads/main.zip
sudo unzip main.zip
sudo rsync --partial -avvz PubData2XL-main/src/* src/.
sudo rm -rf main.zip PubData2XL-main/
pip install -r src/requirements.txt
sudo systemctl restart pubdata2xl && sudo systemctl restart nginx
```

