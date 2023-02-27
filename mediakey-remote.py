# TODO 
# mediakey-remote.py
#
# service install scripts
# - linux
# - windows
# - mac
#
# externalize config
# - controller: 
#
# - global
#   - volume step (default: 1)
#   - refresh
#
# - media keys
#   - lower volume key (default: 114)
#   - raise volume key (default: 115)
#
# - sonos
#   - scan for controller
#
# - spotify
#   - ...

#import importlib
import time
from threading import Thread
import keyboard
import soco
import toml


# global vars
config_path="/home/kbouck/dev/mediakey-remote/mediakey-remote-config.toml"
config = {}
state = ""

# load config
def load_config():
    global config_path
    global config
    with open(config_path, 'r') as f:
       config = toml.load(f)
    print("Loaded config from " + config_path)


# discover sonos devices on network
# - todo: error handling
# - todo: make reconnection loop
def connect():
    global sonos
    global state
    global volume
    global volume_step
    global vol_init_max

    #sonos_speakers = soco.discover()
    #if (len(sonos_speakers) > 0):
    #    print("Discovered sonos speakers:")
    #    for speaker in sonos_speakers:
    #        print(speaker.name)
    #else:
    #    # todo - need reconnection loop
    #    system.exit("No sonos speakers discovered") 
    #sonos = sonos_speakers.pop()

    sonos = soco.discovery.any_soco()
    print("Connected to '" + str(sonos.player_name) + "'")
    # todo - error handling if unsuccessful

    state = ""
    volume = 0
    volume_step  = config['sonos']['vol_step']
    vol_init_max = config['sonos']['vol_init_max']

def play_pause():
    global sonos
    global state
    sonos.pause() if (state == "PLAYING") else sonos.play()
    transport_info = sonos.get_current_transport_info()
    state = transport_info['current_transport_state']

def poll_state():
    global state
    global volume
    while True:
        volume = sonos.volume
        transport_info = sonos.get_current_transport_info() 
        state = transport_info['current_transport_state']
        time.sleep(10)


# map keys to api calls
def map_hotkeys():
    global config
    global sonos
    keyboard.add_hotkey(config['keys']['volume_down'], lambda: sonos.set_relative_volume(volume_step*-1), trigger_on_release=False)
    keyboard.add_hotkey(config['keys']['volume_up'],   lambda: sonos.set_relative_volume(volume_step),    trigger_on_release=False)
    keyboard.add_hotkey(config['keys']['next'],        lambda: sonos.next(),     trigger_on_release=False)
    keyboard.add_hotkey(config['keys']['previous'],    lambda: sonos.previous(), trigger_on_release=False)
    keyboard.add_hotkey(config['keys']['play_pause'],  lambda: play_pause(),     trigger_on_release=False)
    # todo: mute/seek?



load_config()

# main
while True:
    try:
        # connect, or reconnect after exception
        connect()      
        map_hotkeys()

        # start state-polling thread
        poller = Thread(name="Polling Thread", target=poll_state)
        poller.start()
        
        # block app to wait for keyboard events
        keyboard.wait()

    except Exception as e: 
        print("Exception from main:")
        print(e)

    except Error as e: 
        print("Error from main:")
        print(e)

    # sleep a bit to avoid a fast loop during a persistent error situation
    time.sleep(1)

