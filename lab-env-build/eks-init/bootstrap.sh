#!/bin/bash

AWS_ACCESS_KEY=$1
AWS_SECRET_KEY=$2
AWS_REGION=$3

EKS_CLUSTER=$4
EKS_ENDPOINT=$5
EKS_CERTIFICATE=$6
EKS_WORKER_ROLE=$7

export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_KEY
export AWS_DEFAULT_REGION=$AWS_REGION

token=$(aws eks get-token --cluster-name $EKS_CLUSTER | jq -r '.status.token')

cat <<EOT > /tmp/kubeconfig
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: $EKS_CERTIFICATE
    server: $EKS_ENDPOINT
  name: eks-cluster
contexts:
- context:
    cluster: eks-cluster
    user: eks-user
  name: eks-context
current-context: eks-context
kind: Config
preferences: {}
users:
- name: eks-user
  user:
    token: $token
EOT


cat <<EOT > /tmp/aws-auth.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: $EKS_WORKER_ROLE
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes

EOT


kubectl create namespace tetration --kubeconfig=/tmp/kubeconfig
kubectl create serviceaccount tetration --namespace=tetration --kubeconfig=/tmp/kubeconfig
kubectl create clusterrolebinding tetration-role-binding --clusterrole=cluster-admin --serviceaccount=tetration:tetration --namespace=tetration --kubeconfig=/tmp/kubeconfig

kubectl describe secrets --namespace=tetration --kubeconfig=/tmp/kubeconfig | grep 'token:' | tail -n 1 | sed -En "s/token:      //p" > /home/ciscolab/eks-credentials

kubectl apply -f /tmp/aws-auth.yml --kubeconfig=/tmp/kubeconfig

kubectl create namespace sock-shop --kubeconfig=/tmp/kubeconfig
kubectl apply -f /var/eks-init/sock-shop.yml --kubeconfig=/tmp/kubeconfig
kubectl apply -f /var/eks-init/sock-shop-lb.yml --kubeconfig=/tmp/kubeconfig

rm -rf /tmp/kubeconfig
rm -rf /tmp/aws-auth.yml