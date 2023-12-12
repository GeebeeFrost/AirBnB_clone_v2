# This manifest configures a web server for deployment of web_static

$html_file = "
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
"

$nginx_config = "
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;

    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location /hbnb_static/ {
            alias /data/web_static/current/;
    }

    add_header X-Served-By $hostname;

    location /.well-known/acme-challenge/ {
            alias /var/www/html/.well-known/acme-challenge/;
    }

    error_page 404 /custom_404.html;
    location = /custom_404.html {
            root /var/www/html;
            internal;
    }

    location /redirect_me {
            return 301 https://youtube.com;
    }

    location / {
            try_files $uri $uri/ =404;
    }
}"

# Ensure nginx package is installed and running
package { 'nginx':
  ensure => installed,
}

service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Package['nginx'],
}

# Configure firewall to allow Nginx HTTP
exec { 'Allow Nginx HTTP':
  command => '/usr/sbin/ufw allow Nginx',
  path    => ['/bin', '/sbin', '/usr/bin', '/usr/sbin'],
  unless  => '/usr/sbin/ufw status | grep "Nginx HTTP"',
}

# Create necessary directories
file { ['/data/web_static/releases/test', '/data/web_static/releases/shared']:
  ensure => directory,
}

# Create fake HTML
file { '/data/web_static/releases/test/index.html':
  content => $html_file,
}

# Create symbolic link
file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test/',
  force   => true,
  require => File['/data/web_static/releases/test/index/html'],
}

# Set ownership of /data directory
file { '/data':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Modify Nginx config
file { '/etc/nginx/sites-available/default':
  ensure  => present,
  content => $nginx_config,
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# Restart Nginx
exec { 'Restart Nginx':
  command     => '/bin/systemctl restart nginx',
  path        => ['/bin', '/sbin', '/usr/bin', '/usr/sbin'],
  refreshonly => true,
}
