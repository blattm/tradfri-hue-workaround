from phue import Bridge
from time import sleep, time
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TradfriLight():
    def __init__(self, light, delay = 1.0):
        # These to variables specify if lamp needs updating of brightness, colortemp or both
        self.needs_brightness = False
        self.needs_colortemp = False
        self._light = light
        self._last_brightness = light.brightness
        self._last_colortemp = light.colortemp
        self._delay = delay
        self._brightness_has_changed = False
        self._colortemp_has_changed = False
        self._t0 = time()
        logging.info(f"Initialized TradfriLight with light ID {light.light_id} and delay {delay}")

    def check_and_update_brightness(self):
        brightness = self._light.brightness
        logging.debug(f"Checking light ID {self._light.light_id}: current brightness {brightness}, last brightness {self._last_brightness}")

        if self._last_brightness != brightness:
            self._brightness_has_changed = True
            self._t0 = time()
            logging.debug(f"Brightness change detected for light ID {self._light.light_id}: new brightness {brightness}")

        if self._brightness_has_changed and self._t0 + self._delay < time():
            self._light.brightness = brightness
            self._brightness_has_changed = False
            logging.debug(f"Brightness updated for light ID {self._light.light_id}: new brightness {brightness}")

        self._last_brightness = brightness

    def check_and_update_colortemp(self):
        colortemp = self._light.colortemp
        logging.debug(f"Checking light ID {self._light.light_id}: current colortemp {colortemp}, last colortemp {self._last_colortemp}")
        if self._last_colortemp != colortemp:
            self._colortemp_has_changed = True
            self._t0 = time()
            logging.debug(f"Colortemp change detected for light ID {self._light.light_id}: new colortemp {colortemp}")


        if self._colortemp_has_changed and self._t0 + self._delay < time():
            self._light.colortemp = colortemp
            self._colortemp_has_changed = False
            logging.debug(f"Colortemp updated for light ID {self._light.light_id}: new colortemp {colortemp}")

        self._last_colortemp = colortemp

def main(bridge, args):
    tradfri_ids = args.light_ids
    light_list = bridge.get_light_objects()
    tradfri_lights = [TradfriLight(l, delay=args.delay) for l in light_list if l.light_id in tradfri_ids]
    logging.info(f"Started main loop with poll time {args.poll_time}")

    while True:
        for light in tradfri_lights:
            light.check_and_update_brightness()
            light.check_and_update_colortemp()
        sleep(args.poll_time)

def list_lights(b: Bridge):
    # light_list = b.get_light_objects()
    # logging.info('Available lights:')
    # for light in light_list:
    #     logging.info(f'{light.light_id}: {light.name}')
    group_list = b.get_group()
    light_dict = b.get_light_objects(mode="id")
    print()
    for group_id in group_list:
        group = b.get_group(group_id=int(group_id))
        group_name = group["name"]
        logging.info(f"GROUP: {group_name} [{group['type']}]")
        for light_id in group["lights"]:
            light = light_dict[int(light_id)]
            logging.info(f'   {str(light.light_id).zfill(2)}: {light.name}')
        print()

if __name__ == '__main__':
    poll_default = 0.3
    delay_default = 0.3
    parser = argparse.ArgumentParser(description='Workaround script for IKEA Trådfri property update issue on Philips Hue Bridge. Simply run the script with bridge IP and Trådfrid light ID\'s as argument. Remember to push the bridge button before starting the script the first time')
    parser.add_argument('bridge_ip')
    parser.add_argument('light_ids', nargs='*', type=float)
    parser.add_argument('-t', '--poll_time', default=poll_default, type=float, help=f'Set how often the lights are checked for property changes. Value in seconds ({poll_default})')
    parser.add_argument('-d', '--delay',type = float, help=f'How long to wait after attempted change before updating the property. Value in seconds ({delay_default})', default=delay_default)
    parser.add_argument('-l', '--list', action='store_true', required=False, default=False,help='List available lights')
    args = parser.parse_args()

    logging.info(f"Connecting to bridge with IP {args.bridge_ip}")
    b = Bridge(args.bridge_ip)
    b.connect()
    b.get_api()
    logging.info("Connected to bridge")

    if args.list:
        list_lights(b)
    elif len(args.light_ids) > 0:
        logging.info(f"Running main loop with light IDs: {args.light_ids}")
        main(b, args)
    else:
        logging.error('No light IDs provided')
