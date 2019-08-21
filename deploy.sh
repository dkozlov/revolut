#!/usr/bin/env bash
set -euxo pipefail

echo "Creating the persistent volume claim..."
 
kubectl apply -f ./kubernetes/persistent-volume-claim.yml
 
 
echo "Creating the database credentials..."
 
kubectl apply -f ./kubernetes/secret.yml
 
 
echo "Creating the postgres deployment and service..."
 
kubectl apply -f ./kubernetes/postgres-deployment.yml
kubectl apply -f ./kubernetes/postgres-service.yml
kubectl rollout status deployment.apps/postgres 
 
echo "Creating the flask deployment and service..."
 
kubectl apply -f ./kubernetes/flask-deployment.yml
kubectl apply -f ./kubernetes/flask-service.yml
kubectl rollout status deployment.apps/server
