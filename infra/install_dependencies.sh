#!/bin/bash
REPOSITORY=/home/ec2-user

sudo yum update -y
sudo yum install -y python3.11
sudo python3.11 -m ensurepip --default-pip
sudo pip install --upgrade pip
sudo pip install -r $REPOSITORY/requirements.txt
sudo alternatives --install /usr/bin/python python /usr/bin/python3.11 50
