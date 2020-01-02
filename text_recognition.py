# USAGE
# Used: Python2.7.17 - code is working, but is advised to use only for reference.
# instead goto https://www.pyimagesearch.com/ where you will finds a lot of great tutorials
# to get started with image recognition/OCR/Machinelearning
# to start: open cmd and run startme.bat and startme2.bat
# you need access to kubectl get pods..

# import the necessary packages
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import cv2
import subprocess
import time
arr = []
filepath = 'pods.txt'
#add podnames in below file and make sure each podname has a yaml
alowed_podlist_file = 'podlist.txt'
i = 0
index = 0

def decode_predictions(scores, geometry):
   # grab the number of rows and columns from the scores volume, then
   # initialize our set of bounding box rectangles and corresponding
   # confidence scores
   (numRows, numCols) = scores.shape[2:4]
   rects = []
   confidences = []

   # loop over the number of rows
   for y in range(0, numRows):
      # extract the scores (probabilities), followed by the
      # geometrical data used to derive potential bounding box
      # coordinates that surround text
      scoresData = scores[0, 0, y]
      xData0 = geometry[0, 0, y]
      xData1 = geometry[0, 1, y]
      xData2 = geometry[0, 2, y]
      xData3 = geometry[0, 3, y]
      anglesData = geometry[0, 4, y]

      # loop over the number of columns
      for x in range(0, numCols):
         # if our score does not have sufficient probability,
         # ignore it
         if scoresData[x] < args["min_confidence"]:
            continue

         # compute the offset factor as our resulting feature
         # maps will be 4x smaller than the input image
         (offsetX, offsetY) = (x * 4.0, y * 4.0)

         # extract the rotation angle for the prediction and
         # then compute the sin and cosine
         angle = anglesData[x]
         cos = np.cos(angle)
         sin = np.sin(angle)

         # use the geometry volume to derive the width and height
         # of the bounding box
         h = xData0[x] + xData2[x]
         w = xData1[x] + xData3[x]

         # compute both the starting and ending (x, y)-coordinates
         # for the text prediction bounding box
         endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
         endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
         startX = int(endX - w)
         startY = int(endY - h)

         # add the bounding box coordinates and probability score
         # to our respective lists
         rects.append((startX, startY, endX, endY))
         confidences.append(scoresData[x])

   # return a tuple of the bounding boxes and associated confidences
   return (rects, confidences)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str,
   help="path to input image")
ap.add_argument("-east", "--east", type=str,
   help="path to input EAST text detector")
ap.add_argument("-c", "--min-confidence", type=float, default=0.5,
   help="minimum probability required to inspect a region")
ap.add_argument("-w", "--width", type=int, default=640,
   help="nearest multiple of 32 for resized width")
ap.add_argument("-e", "--height", type=int, default=640,
   help="nearest multiple of 32 for resized height")
ap.add_argument("-p", "--padding", type=float, default=0.0,
   help="amount of padding to add to each border of ROI")
args = vars(ap.parse_args())

# load the pre-trained EAST text detector
print("[INFO] loading EAST text detector...")
net = cv2.dnn.readNet(args["east"])

def checkdeployment(arr,text2):
   recognized = True
   index=find_item(text2)
   cv2.rectangle(output, (startX-90, startY+40), (startX-50, startY+46),
      (0, 0, 0), 100)
   if text2 in waitlist:
      cv2.putText(output, text2, (startX-120, startY+15),
         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
      cv2.putText(output, 'deploying ', (startX-120, startY+36),
         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
      cv2.rectangle(output, (startX, startY), (endX, endY),
            (0, 255, 0), 2)
   elif (text2 in deployedlist and startX < 1000 and startY < 500):
      cv2.putText(output, text2, (startX-120, startY+15),
         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
      cv2.putText(output, 'deployed ', (startX-120, startY+36),
         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
      cv2.rectangle(output, (startX, startY), (endX, endY),
            (0, 255, 0), 2)
      if index > -1:
         cv2.putText(output, 'Numpods: '+arr[index][1], (startX-120, startY+48),
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
         cv2.putText(output, 'Status: ' + arr[index][2] , (startX-120, startY+60),
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
         cv2.putText(output, 'Restarts: '+ arr[index][3], (startX-120, startY+72),
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
   elif (startX > 1000 and startY > 500):
      command1 = subprocess.Popen(['delete.bat',text2, ''])
      if text2 in deployedlist:
         deployedlist.remove(text2)
      cv2.putText(output, 'Deleted ', (startX-120, startY+36),
         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
      cv2.rectangle(output, (startX, startY), (endX, endY),
            (0, 0, 255), 2)
   elif ( startX < 1000 or startY < 500):
      waitlist.append(text2)
      command1 = subprocess.Popen(['deploy.bat',text2, ''])
      print('Deploying to kubernetes: ' + text2)

def find_item(key):
   for index, sublist in enumerate(arr):
       if key in sublist[0]:
            return index        

def load_getpods():
   try:
      with open(filepath) as fp:
         line = fp.readline()
         findposready = line.find('READY')
         findposstatus = line.find('STATUS')
         findposrestarts = line.find('RESTARTS')
         cnt = 1
         del arr[:]
         while line:
             line = fp.readline()
             name = line[0:findposready-1]
             ready = line[findposready:findposstatus-1]
             status = line[findposstatus:findposrestarts-1]
             restarts = line[findposrestarts:findposrestarts+3]
             arr.append([])
             arr[-1].append(name)
             arr[-1].append(ready)
             arr[-1].append(status)
             arr[-1].append(restarts)
             cnt += 1
         fp.close()
         time.sleep(1)         
         i += 1
   except Exception as e:
      print("do nothing.")

load_getpods()

alowed_podlist = [line.rstrip('\n') for line in open(alowed_podlist_file)]
print(alowed_podlist)

cam = cv2.VideoCapture(0)
#for better performance comment these deleting from screen only works with below enabled
#cam.set(cv2.CAP_PROP_FRAME_WIDTH,1280);
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT,720);

deployedlist = list()
waitlist = list()
waitcounter = 0
pauseloadpods = 0
while(True):
   if pauseloadpods > 10:
      load_getpods()
      #print("pods loaded")
      pauseloadpods = 0
   pauseloadpods += 1   
   if len(waitlist) > 0:
      waitcounter = waitcounter + 1
   if waitcounter > 10:
      deployedlist.extend(waitlist)
      waitlist[:] = []
      waitcounter = 0
   # Capture frame-by-frame
   ret, image = cam.read()
   #image=frame
   orig = image.copy()
   (origH, origW) = image.shape[:2]

   # set the new width and height and then determine the ratio in change
   # for both the width and height
   (newW, newH) = (args["width"], args["height"])
   rW = origW / float(newW)
   rH = origH / float(newH)

   # resize the image and grab the new image dimensions
   image = cv2.resize(image, (newW, newH))
   (H, W) = image.shape[:2]

   # define the two output layer names for the EAST detector model that
   # we are interested -- the first is the output probabilities and the
   # second can be used to derive the bounding box coordinates of text
   layerNames = [
      "feature_fusion/Conv_7/Sigmoid",
      "feature_fusion/concat_3"]

   # construct a blob from the image and then perform a forward pass of
   # the model to obtain the two output layer sets
   blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
      (123.68, 116.78, 103.94), swapRB=True, crop=False)
   net.setInput(blob)
   (scores, geometry) = net.forward(layerNames)

   # decode the predictions, then  apply non-maxima suppression to
   # suppress weak, overlapping bounding boxes
   (rects, confidences) = decode_predictions(scores, geometry)
   boxes = non_max_suppression(np.array(rects), probs=confidences)

   # initialize the list of results
   results = []

   # loop over the bounding boxes
   for (startX, startY, endX, endY) in boxes:
      # scale the bounding box coordinates based on the respective
      # ratios
      startX = int(startX * rW)
      startY = int(startY * rH)
      endX = int(endX * rW)
      endY = int(endY * rH)

      # in order to obtain a better OCR of the text we can potentially
      # apply a bit of padding surrounding the bounding box -- here we
      # are computing the deltas in both the x and y directions
      dX = int((endX - startX) * args["padding"])
      dY = int((endY - startY) * args["padding"])

      # apply padding to each side of the bounding box, respectively
      startX = max(0, startX - dX)
      startY = max(0, startY - dY)
      endX = min(origW, endX + (dX * 2))
      endY = min(origH, endY + (dY * 2))

      # extract the actual padded ROI
      roi = orig[startY:endY, startX:endX]

      # in order to apply Tesseract v4 to OCR text we must supply
      # (1) a language, (2) an OEM flag of 4, indicating that the we
      # wish to use the LSTM neural net model for OCR, and finally
      # (3) an OEM value, in this case, 7 which implies that we are
      # treating the ROI as a single line of text
      config = ("-l eng --oem 1 --psm 7")
      text = pytesseract.image_to_string(roi, config=config)

      # add the bounding box coordinates and OCR'd text to the list
      # of results
      results.append(((startX, startY, endX, endY), text))

   # sort the results bounding box coordinates from top to bottom
   results = sorted(results, key=lambda r:r[0][1])
   output = orig.copy()
   for ((startX, startY, endX, endY), text) in results:
      recognized = False
      #recognized = True
      text1 = text.encode('ascii', 'ignore').decode('ascii')
      text2 = text1.lower()
      if text2 == 'delete':
        cv2.rectangle(output, (1000, 500), (1280, 720),
         (0, 0, 255), 2)
        cv2.putText(output, 'Delete here..', (startX-100, startY+50),
         cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
      elif text2 in alowed_podlist:
         checkdeployment(arr,text2)           
      if recognized == True :
         cv2.rectangle(output, (startX, startY), (endX, endY),
            (0, 255, 0), 2)

   # show the output image
   cv2.imshow("Text Detection", output)
   cv2.waitKey(80)
   
   if cv2.waitKey(1) & 0xFF == ord('q'):
      break

retval, frame = cam.read()
if retval != True:
    raise ValueError("Can't read frame")

cam.release()

