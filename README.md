# Trådfri Hue Workaround
Workaround Script for fixing brightness and colortemp issue with IKEA Trådfri lights on Philips Hue Bridge. It
works by continuously polling the Hue Bridge to detect change in both properties, then resend update commands
to the Trådfri light after a short period.

## Requirements
You'll need a PC or server where the script can run in the background. 
Install python requirements with
```
poetry install
```
 
## Usage
Simply start the script with Hue Bridge IP and Trådfri light ID's as argument. Press the
bridge button before running it the first time.
```
poetry run python tradfri_hue_workaround.py <bridge_ip> <light_id_1> <light_id_2> ...    
```

You can also list available lights and ID's:
```
poetry run python tradfri_hue_workaround.py <bridge_ip> -l
```


## Background
There's a compatibility issue with IKEA Trådfri lights and Philips Hue Bridge where the brightness and colortemp
are not set correctly when changing scenes. The Hue Bridge will first send a command for change of either of the properties,
then the other. The Trådfri light will not accept any commands while it is busy changing the
first property and discards the command to change the other one. This results in a missmatch where the
Hue Bridge thinks both properties has changed, while it has actually not changed. 

 
