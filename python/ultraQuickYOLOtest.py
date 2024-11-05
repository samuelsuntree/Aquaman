from ultralytics import YOLO

# ---------------------------------------------------------

# Takes a video, apply a YOLO model, and display the result with prebuilt functions

# ---------------------------------------------------------

model = YOLO("C:/Users/10521/Documents/GitHub/Aquaman/runs/segment/bestsiming.pt")
#path = "C:/Users/10521/Documents/GitHub/Aquaman/20240112_f57_crop1.mp4"
path = "G:/fish24Rot.mp4"
model(path, show=True)