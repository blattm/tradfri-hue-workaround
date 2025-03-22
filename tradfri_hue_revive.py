from phue import Bridge
from time import sleep, time
import argparse
import logging
from threading import Thread
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def revive_lamps_sync(*ids):
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Workaround script for IKEA Trådfri property update issue on Philips Hue Bridge. Simply run the script with bridge IP and Trådfrid light ID\'s as argument. Remember to push the bridge button before starting the script the first time')
    parser.add_argument('bridge_ip')
    parser.add_argument('ids',  nargs='*', type=int, default=[], help="Light ids to revive")
    args = parser.parse_args()

    logging.info(f"Connecting to bridge with IP {args.bridge_ip}")
    b = Bridge(args.bridge_ip)
    b.connect()
    b.get_api()
    logging.info("Connected to bridge")

    lights = b.get_light_objects(mode="id")

    for i in range(2):
        revive_lamps_sync(*args.ids)
