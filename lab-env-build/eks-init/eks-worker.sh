#!/bin/bash

AWS_ACCESS_KEY=$1
AWS_SECRET_KEY=$2
AWS_REGION=$3

EKS_WORKER_NAME=$4

export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_KEY
export AWS_DEFAULT_REGION=$AWS_REGION

aws ec2 describe-instances --filters "Name=tag:Name,Values=$EKS_WORKER_NAME*" --output text --query 'Reservations[*].Instances[*].[PrivateIpAddress]'
