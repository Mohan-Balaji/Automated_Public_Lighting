import paho.mqtt.client as mqtt

# Define callback functions for different MQTT events
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("my_topic")
    else:
        print("Connection failed")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")

# Create an MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect("192.168.1.7", 1883, 60)

# Publish a message
client.publish("my_topic", "Hello, MQTT!")

# Listen for messages and handle events
client.loop_forever()
