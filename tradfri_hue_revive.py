from phue import Bridge
from time import sleep, time
import argparse
import logging
from threading import Thread

from settings_by_modelid import SETTINGS_BY_MODELID

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def revive_lamps_sync(b, *ids):
    for i in range(2):
        lights = b.get_light_objects(mode="id")

        params = ["brightness", "colortemp"]
        # params = ["on"]
        # params = []

        states = {}
        for id in ids:
            light = lights[id]
            states[id] = [getattr(light, param) for param in params]

        for id in ids:
            print(f"try revive {id}")
            b.set_light(id, "on", True)
            # b.set_light(id, {"alert": "select"})
            b.set_light(id, {"alert": "lselect"})

        sleep(0.5)

        for id in ids:
            b.set_light(id, {"alert": "none"})

        sleep(0.5)

        for id in ids:
            light = lights[id]
            for i, param in enumerate(params):
                setattr(light, param, states[id][i])

def main(bridge_ip, *ids):
    logging.info(f"Connecting to bridge with IP {bridge_ip}")
    b = Bridge(bridge_ip)
    b.connect()
    b.get_api()
    logging.info("Connected to bridge")

    revive_lamps_sync(b, *ids)

def main_auto_mode(bridge_ip, room:str):
    logging.info(f"Connecting to bridge with IP {bridge_ip}")
    b = Bridge(bridge_ip)
    b.connect()
    b.get_api()
    logging.info("Connected to bridge")

    ids = []
    group_list = b.get_group()
    for group_id in group_list:
        group = b.get_group(group_id=int(group_id))
        group_name = group["name"]
        if group_name == room:
            for light_id in group["lights"]:
                light_dict = b.get_light(light_id=int(light_id))
                model_id = light_dict["modelid"]
                if model_id in SETTINGS_BY_MODELID:
                    settings = SETTINGS_BY_MODELID[model_id]
                    if settings.get("freezes", False):
                        ids.append(int(light_id))

    revive_lamps_sync(b, *ids)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Workaround script for IKEA Trådfri property update issue on Philips Hue Bridge. Simply run the script with bridge IP and Trådfrid light ID\'s as argument. Remember to push the bridge button before starting the script the first time')
    parser.add_argument('bridge_ip')
    parser.add_argument('ids',  nargs='*', type=int, default=[], help="Light ids to revive")
    parser.add_argument('--room', type=str, help="room to revive, overwrites ids")
    args = parser.parse_args()

    if args.room:
        main_auto_mode(args.bridge_ip, args.room)
    else:
        main(args.bridge_ip, *args.ids)
