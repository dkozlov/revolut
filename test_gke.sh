#!/usr/bin/env bash
set -euxo pipefail

export EXTERNAL_IP=`kubectl get services server --output jsonpath='{.status.loadBalancer.ingress[0].ip}'`

curl http://$EXTERNAL_IP/hello/user -d '{"dateOfBirth":"2018-08-12"}' -H "Content-Type: application/json" -X PUT -v
curl http://$EXTERNAL_IP/hello/user -v
curl http://$EXTERNAL_IP/healthz -v
curl http://$EXTERNAL_IP/metrics -v
curl http://$EXTERNAL_IP/readiness -v
