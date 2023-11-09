#!/bin/bash
REPOSITORY=/home/ec2-user

cd $REPOSITORY
sudo uvicorn main:app --host=0.0.0.0 --port=80 --reload