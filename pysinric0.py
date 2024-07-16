import json
from sinric import SinricPro, SinricProConstants
import asyncio
import paho.mqtt.client as mqtt


APP_KEY = "265c9a75-a62c-46f0-81cb-2ae39798ec87"
APP_SECRET = "416f089e-f729-44f1-b16e-b034bfb66127-09ae102a-144d-4950-a97e-a21cf815a9a7"
SWITCH_ID_0 = "664615befb874c7486d401d0"
SWITCH_ID_1 = "6667baed5d818a66fab79d21"
SWITCH_ID_2 = "6667bb4c6e1af3593503861b"

broker_address = "mqtt.tanam.software"
port = 8883
username = "tanam-broker"
password = "t4nAm_br0k3r"
topic = "tanam1/subscriber"


def power_state(device_id, state):
    if device_id == SWITCH_ID_0:
        # print("relay_ch: {} device_id: {} state: {}".format("0", device_id, state))
        # message = {"relay_ch": "0", "device_id": device_id, "state": state}
        # mqtt_message = json.dumps(message)
        # mqtt_client.publish(topic, mqtt_message)
        for i in range(9):
            relay_ch = str(i)
            print("relay_ch: {} device_id: {} state: {}".format(relay_ch, device_id, state))
            message = {"relay_ch": relay_ch, "device_id": device_id, "state": state}
            mqtt_message = json.dumps(message)
            mqtt_client.publish(topic, mqtt_message)
    elif device_id == SWITCH_ID_1:
        print("relay_ch: {} device_id: {} state: {}".format("1", device_id, state))
        message = {"relay_ch": "1", "device_id": device_id, "state": state}
        mqtt_message = json.dumps(message)
        mqtt_client.publish(topic, mqtt_message)
    elif device_id == SWITCH_ID_2:
        print("relay_ch: {} device_id: {} state: {}".format("2", device_id, state))
        message = {"relay_ch": "2", "device_id": device_id, "state": state}
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
        [SWITCH_ID_0, SWITCH_ID_1, SWITCH_ID_2],
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
