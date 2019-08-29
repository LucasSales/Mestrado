from os import path

import yaml

from kubernetes import client, config

DEPLOYMENT_NAME = "nginx-deployment"

def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()

#     with open(path.join(path.dirname(__file__), "nginx-deployment.yaml")) as f:
#         dep = yaml.safe_load(f)
#         k8s_apps_v1 = client.AppsV1Api()
#         resp = k8s_apps_v1.create_namespaced_deployment(
#             body=dep, namespace="default")
#         print("Deployment created. status='%s'" % resp.metadata.name)

# def delete_deployment(api_instance):
    # Delete deployment
    k8s_apps_v1 = client.AppsV1Api()
    api_response = k8s_apps_v1.delete_namespaced_deployment(
        name=DEPLOYMENT_NAME,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Deployment deleted. status='%s'" % str(api_response.status))        


if __name__ == '__main__':
    main()
    