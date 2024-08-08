from blynklib import Blynk

# Initialize Blynk
BLYNK_AUTH_TOKEN = "MzVdSyFtnA7Ee69hqZGZQm0_eR-rh3py"
blynk = Blynk(BLYNK_AUTH_TOKEN)

# Virtual Pin number you want to write to
VIRTUAL_PIN = 5

# Value to send (0 or 1)
value_to_send = 1  # Change this to 0 if you want to send 0

# Function to send the value
@blynk.handle_event('write V5')
def send_value():
    blynk.virtual_write_msg(VIRTUAL_PIN, value_to_send)
    print(f"Value '{value_to_send}' sent to Blynk V{VIRTUAL_PIN}.")

# Start the Blynk connection
blynk.run()

# Call the send_value function to send the value
send_value()
