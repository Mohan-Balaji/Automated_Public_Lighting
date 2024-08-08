import cv2
import time
import threading
import websocket
import numpy as np

motion_detected = False
connected = False
websocket_url = "ws://192.168.1.100:80/ws"

# Create a background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

# Function to establish WebSocket connection
def establish_websocket_connection():
    global ws, connected
    try:
        ws = websocket.WebSocketApp(websocket_url,
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_close=on_close,
                                    on_error=on_error)
        ws.run_forever()
    except Exception as e:
        print("Error establishing WebSocket connection:", e)
        connected = False

# Event handler for WebSocket connection open
def on_open(ws):
    global connected
    print("Connected to WebSocket server")
    connected = True

# Event handler for WebSocket messages received from the server
def on_message(ws, message):
    print("Received message:", message)

# Event handler for WebSocket connection close
def on_close(ws):
    global connected
    print("Connection closed")
    connected = False
    # Attempt to reconnect
    establish_websocket_connection()

# Event handler for WebSocket errors
def on_error(ws, error):
    global connected
    print("WebSocket error:", error)
    connected = False
    # Attempt to reconnect
    establish_websocket_connection()

# Function to send motion detection status via WebSocket
def send_motion_status():
    global motion_detected, ws, connected
    while True:
        try:
            if connected:
                if motion_detected:
                    ws.send('1')
                    print("Motion Detected!")
                    motion_detected = False
                    time.sleep(5)                                           # Timer For delay adjust in (seconds)
                    ws.send('0')
                else:
                    print("Motion not detected")
        except Exception as e:
            print("Error sending motion status via WebSocket:", e)
            connected = False
            # Attempt to reconnect
            establish_websocket_connection()

# Start the WebSocket connection thread
websocket_thread = threading.Thread(target=establish_websocket_connection)
websocket_thread.start()

# Start the motion detection thread
motion_detection_thread = threading.Thread(target=send_motion_status)
motion_detection_thread.start()

# Initialize the camera or video feed
cap = cv2.VideoCapture(0)  # Use 0 for the default camera or specify a video file path

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply the background subtractor to the current frame
    fgmask = fgbg.apply(frame)

    # Remove noise and smooth the result
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel=np.ones((5, 5), np.uint8))

    # Find contours in the foreground mask
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contour has an area greater than a threshold (motion detected)
    motion_detected = False
    count = 0
    for contour in contours:
        if cv2.contourArea(contour) > 3000:  # Adjust this threshold as needed
            motion_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the original frame with motion detected
    cv2.imshow('Motion Detection', frame)
    
    if cv2.waitKey(30) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
