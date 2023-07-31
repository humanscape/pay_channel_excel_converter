#!/bin/bash
REPOSITORY=/home/ec2-user

echo $(sudo uvicorn main:app --host=0.0.0.0 --port=80 --reload)