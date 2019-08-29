# Config Infra

### Install Docker
```
 sudo apt-get update \ 
 && sudo apt-get install -qy docker.io
```

### Install Kubernetes apt repo
```
  sudo apt-get update \
  && sudo apt-get install -y apt-transport-https \
  && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
```

```
  echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" \
  | sudo tee -a /etc/apt/sources.list.d/kubernetes.list \
  && sudo apt-get update 
```
- Now install kubelet, kubeadm and kubernetes-cni

```
 sudo apt-get update \
  && sudo apt-get install -y \
  kubelet \
  kubeadm \
  kubernetes-cni
```

### Swap must be disabled!!

- sudo swapoff -a

### Execute kubeadm

```
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=<IP_YOUR_HOST> --kubernetes-version stable-1.11
```

### After running kubeadm, run:

```
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

```
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

```
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/k8s-manifests/kube-flannel-rbac.yml
```

### By default, containers can not run on major nodes in the cluster. If you want the main node to run its containers, run the command:
```
kubectl taint nodes --all node-role.kubernetes.io/master-
```

# SPI AFIS Webservice 

### SPI AFIS Webservice PRE SETTINGS Using Docker and Kubernetes:
- Add in your pom.xml
  ```
  <dependency>
     <groupId>org.postgresql</groupId>
     <artifactId>postgresql</artifactId>
     <scope>runtime</scope>
  </dependency>
  ```
-  Replace in your applications.properties the spring.datasource.url, spring.datasource.username and spring.datasource.password by:
  ```
  O nome do database é o mesmo que é colocado no database.yml
  spring.datasource.url=jdbc:postgresql://${POSTGRES_HOST}:5432/${DATABASE_NAME}  
  spring.datasource.username=${POSTGRES_USER}
  spring.datasource.password=${POSTGRES_PASSWORD}
  ```
- Install maven and run command: 
  `mvn -N io.takari:maven:wrapper`

- After run command:
  `./mvnw -DskipTests package`

- Create your Dockerfile
```
  FROM openjdk:8-jdk-alpine
  COPY target/<YOUR_JAR>.jar /app.jar
  EXPOSE 8085/tcp
  ENTRYPOINT ["java", "-jar", "/app.jar"]
```
- Run command: 
  `sudo docker build -t <NAME_YOUR_IMAGE>:<TAG_YOUR_IMAGE> <LOCAL_DOCKERFILE>`

- Add your docker image to your dockerhub repository                                                                              
  ```
  sudo docker tag <NAME_IMAGE>:<TAG> <YOUR_ACCOUNT_NAME_DOCKERHUB>/<TAG>
  sudo docker push <YOUR_ACCOUNT_NAME_DOCKERHUB>/<TAG>
  ```

### How To Run Using Local Postgres

First: 

- Clone o repositório do metrics-server https://github.com/kubernetes-incubator/metrics-server.git
- Dentro da pasta do metrics-server, procure a pasta deploy/1.8+/
- Abra o arquivo metrics-server-deployment.yaml e cole o seguinte comando em spec/template/spec/containers:
```
  - command:
    - /metrics-server
    - --kubelet-insecure-tls
    - --kubelet-preferred-address-types=InternalIP
```
- Execute o comando `kubectl create -f deploy/1.8+/`

Second:
In your git project inside the config/ folder, run:

- Configure o arquivo config-map.yml para que seu serviço consiga acessar o Postgres
- `kubectl create -f config-map.yml`
- `kubectl create -f replicaset.yml.yml`
- Autoscale: `kubectl autoscale rs webservice-rs --cpu-percent=50 --min=1 --max=3`
- Scale manually: `kubectl scale rs webservice --replicas=3`

### How To Run Using Postgres Pod

First: 
Remova do config-map.yml a linha postgres_host

- `kubectl create -f database.yml`

Second:

- `NAME_YOUR_HOST = webservice-hostname`
- `NAME_YOUR_DB_SERVICE = postgres`
- `kubectl create configmap <NAME_YOUR_HOST> --from-literal=postgres_host=$(kubectl get svc <NAME_YOUR_DB_SERVICE> -o jsonpath="{.spec.clusterIP}")`

Third:
- `kubectl create -f webservice.yml`

Fourth:
- Before this step, install metrics-server k8s
- `kubectl expose deployment <NAME-YOUR-DEPLOYMENT> --type=LoadBalancer --port=8080`
- Scale manually: `kubectl scale deployment <NAME-YOUR-DEPLOYMENT> --replicas=3`
- Autoscale: `kubectl autoscale deployment <NAME-YOUR-DEPLOYMENT> --cpu-percent=50 --min=1 --max=10`

### How Update Image

- `kubectl set image deployment/<NAME_DEPLOYMENT> <NAME_IMAGE>=<your Docker Hub account>/<NEW_IMAGE_NAME>:<TAG_NAME>`

### How Delete All

- `kubectl delete -f <FILE.yml>`
- `kubectl delete svc <SERVICE_NAME>`
- `kubectl delete cm <CONFIGMAP_NAME>`

### Useful Commands

- `kubectl get deployments`
- `kubectl get pods`
- `kubectl get svc`
- `kubectl get cm`
- `kubectl get pvc`
- `kubectl get hpa`
- `kubectl get sc`
- `kubectl get all -n kube-system`
- `kubectl delete hpa <NAME>`
- `kubectl exec -it <nome_pod> bash`
- `kubectl logs --previous <name-pod> Ver erros depois de um pod parar de funcionar`
- `kubectl logs <name-pod> mostra os logs daquele momento de um pod`
- `kubeadm reset`
- `kubeadm token create --print-join-command`
- `kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep <NAME-USER> | awk '{print $1}')`
- `kubeadm token create --print-join-command`
- `kubectl edit -n <NOME_DO_NAMESPACE> [TIPO, QUE PODE SER <service, deploy, hpa, pod, etc.>]<NOME_DO_TIPO_QUE_VOCE_QUER_EDITAR>`

### Para executar no localhost utilizando minikube é necessário realizar os seguintes comandos:
- Install minikube https://kubernetes.io/docs/tasks/tools/install-minikube/
- Run commands: 
  ```
  minikube start
  kubectl config use-context minikube
  eval $(minikube docker-env)
  ```

# Install Dashboad and Metrics-Server for k8s

### Create service account

- Create file service-account.yaml

```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: <NAME_USER>
  namespace: kube-system <ADD-NAME-SPACE>
```

### Create Role-based access control (RBAC) for the user you created in the previous step

- Create file rbac.yaml
```
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kube-system
```
### Execute files and deploy dashboard

- Run: 
```
  kubectl create -f service-account.yaml
  kubectl create -f rbac.yaml
  kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
```

### Configure NondePort for your dashboard

- Execute:
```
  kubectl -n kube-system edit svc kubernetes-dashboard
```
- You should see yaml representation of the service. 
- Change type: ClusterIP to type: NodePort and add save file.

### To access the dashboard, run:

- Run
```
kubectl -n kube-system get svc kubernetes-dashboard
```
- You should see the node port of your dashboard

- In your browser access: http://<IP_YOUR_MASTER>:<NODE_PORT_DASHBOARD>

- Select option token

### GET TOKEN for the user created in the first step
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep <NAME-USER> | awk '{print $1}')

### Metrics-Server

- Clone repository metrics-server
```
https://github.com/kubernetes-incubator/metrics-server.git
```
- In folder deploy/1.8+/ change file metrics-server-deployment.yaml and add in spec/template/spec/containers
```
command:
  - /metrics-server
  - --kubelet-preferred-address-types=InternalIP
  - --kubelet-insecure-tls
```
- Run

```
kubectl create -f deploy/1.8+/
```

### Desenvolvedor: Lucas Sales