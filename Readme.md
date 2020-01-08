# Kubernetes deployments through whiteboard and OCR using Tesseract.js

## Update 08/01/2020: 
I containerized the demo, now so it is much easier to load the demo through minikube for example. <br>

Screenshot from the containerized version: <br>
![](/screenshot.jpg)

To do that I had to switch to nodejs with tesseract.js but the OCR is working and I added helm deploy example. So 'helm mariadb' fetches helm chart from stable and deploys. <br>
The container serves the client/webcam app and in the backend it deploys via kubectl and helm3 which are also in the image (see dockerfile) <br>

The demo is restricted to these words as it is only an experiment: "grafana", "nginx", "stellar", "tensorflow", "mysql", "helm mariadb", "artifactory", "prometheus", "wordpress" <br>
This can be changed in the index.html <br>

### Deployment instructions
kubectl apply -f 1-deployment.yaml <br>
kubectl apply -f 2-service.yaml <br>
minikube service helm3-kubectl-node --https <br>
(That should open your browser. Container is running on 8443 https) <br>

The movie below was originally created with the python code which is still in the python branch. But that requires you to setup python with the modules etc. <br>
![](/opencvtesseract.gif)

