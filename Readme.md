# A nodejs container with OCR using Tesseract.js

## Update 08/01/2020: 
Demo is containerized now, so it is much easier to load the demo through minikube for example. <br>

Screenshot from the container version: <br>
![](/screenshot.jpg)

Switched from python to nodejs with tesseract.js. The OCR is less accurate then the python one which preprocesses with Opencv. <br> 
You can also test it with text on your phone (see phone.jpg) <br> 
The container serves the client app and in the backend it deploys via kubectl and helm3. <br>

The demo is restricted to these words: "grafana", "nginx", "stellar", "tensorflow", "mysql", "helm mariadb", "artifactory", "prometheus", "wordpress" <br>
This can be changed in the index.html <br>

### Deployment instructions
kubectl apply -f 1-deployment.yaml <br>
kubectl apply -f 2-service.yaml <br>
minikube service helm3-kubectl-node --https <br>
(That should open your browser. Container is running on 8443 https https://localhost:8443/) <br>

The movie below was originally created with the python code which is still in the python branch. But that requires you to setup python with the modules etc. <br>
![](/opencvtesseract.gif)
