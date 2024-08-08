import requests

# Replace with your ESP8266's local IP address
esp8266_ip = "192.168.1.100"

# Send data (0 or 1) to ESP8266
def send_data_to_esp(data_to_send):
    url = f"http://{esp8266_ip}/set"
    payload = {"value": data_to_send}
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("Data sent successfully to ESP8266.")
    else:
        print("Failed to send data to ESP8266.")

# Send data to ESP8266 (0 or 1)
data_to_send = 1 # Change this value to 0 or 1
send_data_to_esp(data_to_send)
