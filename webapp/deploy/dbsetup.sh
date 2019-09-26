#!/bin/sh

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

if [  -n "$(uname -a | grep Ubuntu)" ]; then
    # OS is Ubuntu
    apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8
    add-apt-repository 'deb [arch=amd64,arm64,ppc64el] http://ftp.utexas.edu/mariadb/repo/10.3/ubuntu bionic main'
    apt update
    apt install mariadb-server -y


else
    # Instructions for Centos/ Fedora/ RHEL
    echo "yum installation"
    DEST_DIR=/etc/yum.repos.d/MariaDB.repo
    REPO=$(cat <<-EOF
[mariadb]
name = MariaDB
baseurl = http://yum.mariadb.org/10.3/centos7-amd64
gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=1
EOF
)
    echo "$REPO" > "$DEST_DIR"

    yum clean all
    rpm --import https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
    yum install MariaDB-server -y


fi

systemctl enable mariadb
systemctl start mariadb

mysql_secure_installation
#systemctl status mariadb