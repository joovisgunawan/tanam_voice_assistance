import json
from sinric import SinricPro, SinricProConstants
import asyncio
import paho.mqtt.client as mqtt


APP_KEY = "2087fa18-adb1-4694-824e-31191b727818"
APP_SECRET = "b0d31a6b-147e-409d-a7b8-cff441b0f682-c1e814fa-d29b-4357-b83b-3fd699e1880a"
SWITCH_ID_6 = "6669b6365d818a66fab84fb2"
SWITCH_ID_7 = "6669b64d5d818a66fab84fd1"
SWITCH_ID_8 = "6669b65f5d818a66fab84ff0"

broker_address = "mqtt.tanam.software"
port = 8883
username = "tanam-broker"
password = "t4nAm_br0k3r"
topic = "tanam1/subscriber"


def power_state(device_id, state):
    if device_id == SWITCH_ID_6:
        print("relay_ch: {} device_id: {} state: {}".format("6", device_id, state))
        message = {"relay_ch": "6", "device_id": device_id, "state": state}
        mqtt_message = json.dumps(message)
        mqtt_client.publish(topic, mqtt_message)
    elif device_id == SWITCH_ID_7:
        print("relay_ch: {} device_id: {} state: {}".format("7", device_id, state))
        message = {"relay_ch": "7", "device_id": device_id, "state": state}
        mqtt_message = json.dumps(message)
        mqtt_client.publish(topic, mqtt_message)
    elif device_id == SWITCH_ID_8:
        print("relay_ch: {} device_id: {} state: {}".format("8", device_id, state))
        message = {"relay_ch": "8", "device_id": device_id, "state": state}
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
        [SWITCH_ID_6, SWITCH_ID_7, SWITCH_ID_8],
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
