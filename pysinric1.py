import json
from sinric import SinricPro, SinricProConstants
import asyncio
import paho.mqtt.client as mqtt


APP_KEY = "28e51ba8-cede-4c24-bcaa-5125547114d9"
APP_SECRET = "8d855f1f-f57b-45ec-99f9-d24f985bc99e-3dff84bc-caa0-4c92-b2b4-6912cadd0a34"
SWITCH_ID_3 = "665e8c19888aa7f7a233449f"
SWITCH_ID_4 = "6667bbe4674e208e6fe60634"
SWITCH_ID_5 = "6667bbfc5d818a66fab79e75"

broker_address = "mqtt.tanam.software"
port = 8883
username = "tanam-broker"
password = "t4nAm_br0k3r"
topic = "tanam1/subscriber"


def power_state(device_id, state):
    if device_id == SWITCH_ID_3:
        print("relay_ch: {} device_id: {} state: {}".format("3", device_id, state))
        message = {"relay_ch": "3", "device_id": device_id, "state": state}
        mqtt_message = json.dumps(message)
        mqtt_client.publish(topic, mqtt_message)
    elif device_id == SWITCH_ID_4:
        print("relay_ch: {} device_id: {} state: {}".format("4", device_id, state))
        message = {"relay_ch": "4", "device_id": device_id, "state": state}
        mqtt_message = json.dumps(message)
        mqtt_client.publish(topic, mqtt_message)
    elif device_id == SWITCH_ID_5:
        print("relay_ch: {} device_id: {} state: {}".format("5", device_id, state))
        message = {"relay_ch": "5", "device_id": device_id, "state": state}
        mqtt_message = json.dumps(message)
        mqtt_client.publish(topic, mqtt_message)
    else:
        print("device_id not found!")

    return True, state


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Failed to connect, return code: {reason_code}")


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.username_pw_set(username, password)
mqtt_client.tls_set()
mqtt_client.on_connect = on_connect

try:
    mqtt_client.connect(broker_address, port, 60)
except Exception as e:
    print(f"Error connecting to broker: {e}")
    exit()

callbacks = {SinricProConstants.SET_POWER_STATE: power_state}


async def main():
    client = SinricPro(
        APP_KEY,
        [SWITCH_ID_3, SWITCH_ID_4, SWITCH_ID_5],
        callbacks,
        enable_log=False,
        restore_states=False,
        secret_key=APP_SECRET,
    )
    await client.connect()


# if __name__ == "__main__":
#     # loop = asyncio.new_event_loop()
#     # asyncio.set_event_loop(loop)
#     loop = asyncio.get_event_loop()
#     client = SinricPro(
#         APP_KEY,
#         [SWITCH_ID_1, SWITCH_ID_2, SWITCH_ID_3],
#         callbacks,
#         enable_log=False,
#         restore_states=False,
#         secret_key=APP_SECRET,
#     )
#     loop.run_until_complete(client.connect())

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.create_task(main())

    # Integrate the MQTT loop with asyncio
    mqtt_client.loop_start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Exiting...")
    # finally:
    #     mqtt_client.loop_stop()
    #     loop.stop()
