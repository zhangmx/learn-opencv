import cv2

# 检测可用摄像头
def list_cameras():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr

# 列出所有可用摄像头
available_cameras = list_cameras()
print("Available cameras:", available_cameras)

# 选择要使用的摄像头
if len(available_cameras) > 0:
    cam_id = int(input(f"Select camera ID from {available_cameras}: "))
else:
    print("No available cameras found")
    exit()

# 创建VideoCapture对象
cap = cv2.VideoCapture(cam_id)

# 检查相机是否已成功打开
if not cap.isOpened():
    print(f"Cannot open camera {cam_id}")
    exit()

while True:
    # 捕捉视频帧
    ret, frame = cap.read()

    # 如果帧读取正确，ret为True
    if not ret:
        print("Cannot receive frame (stream end?). Exiting ...")
        break

    # 显示帧
    cv2.imshow('Video Frame', frame)

    # 按下'q'键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放VideoCapture对象
cap.release()
# 关闭所有OpenCV窗口
cv2.destroyAllWindows()
