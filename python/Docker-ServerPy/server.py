from flask import Flask

from os import path

from kubernetes import client, config

import yaml

app = Flask(__name__)

DEPLOYMENT_NAME = "nginx-deployment"


@app.route("/")
def hello():
    return "Hello from Python!"


def create_deployment_object():
    # Configureate Pod template container
    container = client.V1Container(
        name="nginx",
        image="nginx:1.15.4",
        ports=[client.V1ContainerPort(container_port=80)])
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=3,
        template=template,
        selector={'matchLabels': {'app': 'nginx'}})
    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec)

    return deployment

@app.route("/create")
def create_deploy():

	config.load_kube_config()

	with open(path.join(path.dirname(__file__), "nginx-deployment.yaml")) as f:
		dep = yaml.safe_load(f)
		k8s_apps_v1 = client.AppsV1Api()
		resp = k8s_apps_v1.create_namespaced_deployment(body=dep, namespace="default")
		return ("Deployment created. status='%s'" % resp.metadata.name)

@app.route("/delete/<nameDeploy>")
def delete_deployment(nameDeploy):
    # Delete deployment
	config.load_kube_config()

	k8s_apps_v1 = client.AppsV1Api()
	resp = k8s_apps_v1.delete_namespaced_deployment(
        name=nameDeploy,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
	return ("Deployment deleted. status='%s'" % str(resp.status))    

if __name__ == "__main__":
    app.run(host='0.0.0.0')
