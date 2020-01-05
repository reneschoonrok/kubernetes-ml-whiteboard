# Kubernetes deployments through whiteboard and machinelearning OCR

# Update 05/01/2020: Progressing very well on a fully containerized solution using alpine + kubectl + helm3 + Nodejs + Tesseract.js
(all in one container, no client python install or anything needed anymore, I will push the repo and Dockerfile soon)

An experiment trying to make kubernetes deployments easier with machine learning
This uses: Python 2.7, Opencv2 and TesseractOCR. The training set for characters is provided also as a large file.

You can use stickers, t-shirts and text-notes ;)
It can deploy to and delete from kubernetes (turn up the resolution to 720p for the camera for delete. see in code)

![](/opencvtesseract.gif)

### Credits.. <br/>
 <br/>
pyimagesearch for the ML code  <br/>
Do not take my code as a starting point. Instead go to below website and get properly started. <br/>
https://pyimagesearch.com <br/>
