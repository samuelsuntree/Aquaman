from ultralytics import YOLO
import cv2

# 初始化模型和视频路径
model = YOLO("C:/Users/10521/Documents/GitHub/Aquaman/runs/segment/train640_32_500_manuel/weights/best.pt")
path = "C:/Users/10521/Documents/GitHub/Aquaman/T4_Fish3_C2_270923 - Trim2.mp4"
cap = cv2.VideoCapture(path)
model(path, show=True)
# 用于记录鱼出现的时间段
fish_times = []
start_time = None

# 处理视频帧
while True:
    ret, frame = cap.read()
    if not ret:
        break
    results = model(frame)

    # 检测到的对象的置信度大于0.6时记录时间
    fish_detected = False
    if hasattr(results, 'boxes') and hasattr(results.boxes, 'xyxy') and len(results.boxes.xyxy) > 0:
        for detection in results.boxes.xyxy[0]:
            x1, y1, x2, y2, conf, cls_id = detection[:6]
            if cls_id == model.names.index('fish') and conf > 0.6:
                fish_detected = True
                if start_time is None:
                    start_time = cap.get(cv2.CAP_PROP_POS_MSEC)  # 获取当前帧的时间戳（毫秒）
                print("Fish found")  # 检测到鱼时打印
                break  # 如果只关心是否有任何检测满足条件，则检测到第一个后即可跳出循环

    if not fish_detected and start_time is not None:
        # 当前帧未检测到或视频结束，且之前已开始记录时间
        end_time = cap.get(cv2.CAP_PROP_POS_MSEC)
        fish_times.append((start_time, end_time))
        start_time = None

# 检查是否有正在记录的时间段
if start_time is not None:
    end_time = cap.get(cv2.CAP_PROP_POS_MSEC)
    fish_times.append((start_time, end_time))

# 释放视频捕捉对象
cap.release()

# 输出鱼出现的时间段
print("Fish appeared in the following time intervals (in milliseconds):")
for start, end in fish_times:
    print(f"From {start} to {end}")
