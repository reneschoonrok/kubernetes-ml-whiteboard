FOR /L %%A IN (1,1,1000) DO (
   cls
   Echo -----------------------
   Echo - kubectl get pods    -
   Echo -----------------------
   kubectl get pods
   Echo -----------------------
   Echo - kubectl get volumes -
   Echo -----------------------
   kubectl get pvc
   del pods.txt
   kubectl get pods >>pods.txt
   timeout 3
)