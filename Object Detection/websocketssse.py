import websocket
import time

# WebSocket server address
ws_url = "ws://192.168.1.100:80/ws"

# Event handler for WebSocket connection open
def on_open(ws):
    print("Connected to WebSocket server")
    # Send a message to the server once the connection is open
    for i in range(10):
        if i%2==0:
            ws.send('0')
            time.sleep(2)
        else:
            ws.send('1')
            time.sleep(2)

# Event handler for WebSocket messages received from the server
def on_message(ws, message):
    print("Received message:", message)

# Event handler for WebSocket connection close
def on_close(ws):
    print("Connection closed")

# Event handler for WebSocket errors
def on_error(ws, error):
    print("WebSocket error:", error)

# Create a WebSocket connection
ws = websocket.WebSocketApp(ws_url,
                            on_open=on_open,
                            on_message=on_message,
                            on_close=on_close,
                            on_error=on_error)

# Run the WebSocket client
ws.run_forever()

