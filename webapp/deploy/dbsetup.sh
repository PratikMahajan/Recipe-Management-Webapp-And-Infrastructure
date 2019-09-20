#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

if [  -n "$(uname -a | grep Ubuntu)" ]; then
    # OS is Ubuntu
    sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8

    sudo add-apt-repository 'deb [arch=amd64,arm64,ppc64el] http://ftp.utexas.edu/mariadb/repo/10.3/ubuntu bionic main'

    sudo apt update

    sudo apt install mariadb-server

    sudo systemctl status mariadb

else
    # Instructions for Centos/ Fedora/ RHEL


fi