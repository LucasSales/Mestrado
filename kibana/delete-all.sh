#!/bin/bash

kubectl delete -f es-statfulset.yaml -f es-svc.yaml
kubectl delete -f kibana-deploy.yaml -f kibana-svc.yaml
kubectl delete -f fluentd/fluentd-configmap.yml -f fluentd/fluentd-es-ds.yml
