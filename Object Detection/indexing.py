import cv2

def list_camera_indices():
    camera_indices = []
    for index in range(10):  # Try indices from 0 to 9
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            camera_indices.append(index)
            cap.release()
    return camera_indices

camera_list = list_camera_indices()
if len(camera_list) > 0:
    print("Available camera indices:")
    for index in camera_list:
        print(f"Camera Index: {index}")
else:
    print("No cameras found.")
