from ultralytics import YOLO

# ---------------------------------------------------------

# Takes a video, apply a YOLO model, and display the result with prebuilt functions

# ---------------------------------------------------------

model = YOLO("C:/Users/10521/Documents/GitHub/Aquaman/runs/segment/train640_32_500_manuel/weights/best.pt")
path = "C:/Users/10521/Documents/GitHub/Aquaman/T4_Fish3_C2_270923 - Trim2.mp4"

model(path, show=True)