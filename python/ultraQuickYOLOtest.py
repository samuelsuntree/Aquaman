from ultralytics import YOLO

# ---------------------------------------------------------

# Takes a video, apply a YOLO model, and display the result with prebuilt functions

# ---------------------------------------------------------

model = YOLO("C:/Users/blagn771/Documents/Aquaman/Aquaman/runs/segment/train640_32_500_manuel/weights/best.pt")
path = "C:/Users/blagn771/Desktop/simingFlipCrop.mp4"

model(path, show=True)