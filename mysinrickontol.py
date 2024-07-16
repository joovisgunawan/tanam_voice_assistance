from sinric import SinricPro, SinricProConstants
import asyncio

APP_KEY = "265c9a75-a62c-46f0-81cb-2ae39798ec87"
APP_SECRET = "416f089e-f729-44f1-b16e-b034bfb66127-09ae102a-144d-4950-a97e-a21cf815a9a7"
SWITCH_ID_1 = "664615befb874c7486d401d0"
SWITCH_ID_2 = "6667baed5d818a66fab79d21"
SWITCH_ID_3 = "6667baed5d818a66fab79d21"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Failed to connect, return code: {rc}")

def power_state(device_id, state):
    if device_id == SWITCH_ID_1:
        print('device_id: {} state: {}'.format(device_id, state))
    elif device_id == SWITCH_ID_2:
        print('device_id: {} state: {}'.format(device_id, state))
    else:
        print("device_id not found!")

    return True, state


callbacks = {
    SinricProConstants.SET_POWER_STATE: power_state
}

if __name__ == '__main__':
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [SWITCH_ID_1, SWITCH_ID_2], callbacks,
                       enable_log=False, restore_states=False, secret_key=APP_SECRET)
    loop.run_until_complete(client.connect())

    # To update the power state on server.
    # client.event_handler.raise_event(SWITCH_ID, SinricProConstants.SET_POWER_STATE, data = {SinricProConstants.STATE: SinricProConstants.POWER_STATE_ON })
    # client.event_handler.raise_event(SWITCH_ID, SinricProConstants.SET_POWER_STATE, data = {SinricProConstants.STATE: SinricProConstants.POWER_STATE_OFF })