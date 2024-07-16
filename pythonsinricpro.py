import asyncio
import json
from mysinrickontol import SinricPro, SinricProConstants
import paho.mqtt.client as mqtt

# SinricPro credentials
APP_KEY = "265c9a75-a62c-46f0-81cb-2ae39798ec87"
APP_SECRET = "416f089e-f729-44f1-b16e-b034bfb66127-09ae102a-144d-4950-a97e-a21cf815a9a7"
SWITCH_ID_1 = "664615befb874c7486d401d0"
SWITCH_ID_2 = "6667baed5d818a66fab79d21"
SWITCH_ID_3 = "6667baed5d818a66fab79d21"

# # MQTT broker details
# broker_address = "mqtt.tanam.software"
# port = 8883
# username = "tanam-broker"
# password = "t4nAm_br0k3r"
# topic = "your/mqtt/topic"  # Replace with your MQTT topic

# Initialize MQTT client
# mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# mqtt_client.username_pw_set(username, password)
# mqtt_client.tls_set()

# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("Connected to MQTT broker")
#     else:
#         print(f"Failed to connect, return code: {rc}")

# mqtt_client.on_connect = on_connect

# try:
#     mqtt_client.connect(broker_address, port)
# except Exception as e:
#     print(f"Error connecting to broker: {e}")
#     exit()

def power_state(device_id, state):
    message = {"device_id": device_id, "state": state}
    
    if device_id in [SWITCH_ID_1, SWITCH_ID_2, SWITCH_ID_3]:
        print(f"device_id: {device_id} state: {state}")
        # mqtt_message = json.dumps(message)
        # mqtt_client.publish(topic, mqtt_message)
    else:
        print("device_id not found!")
    
    return True, state

callbacks = {SinricProConstants.SET_POWER_STATE: power_state}

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    client = SinricPro(
        APP_KEY,
        [SWITCH_ID_1, SWITCH_ID_2, SWITCH_ID_3],
        callbacks,
        enable_log=False,
        restore_states=False,
        secret_key=APP_SECRET,
    )
    loop.run_until_complete(client.connect())
    # mqtt_client.loop_start()
