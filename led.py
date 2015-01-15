import RPi.GPIO as gpio
import time
import argparse
import copy
import random
import sys
import itertools

chan_dict = {'red':{'color': 'red', 'pin': 7, 'max':100, 'min':40},
        'blue':{'color': 'blue', 'pin': 11, 'max': 80, 'min': 30},
        'green':{'color': 'green', 'pin': 16, 'max': 100, 'min':40}}

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setwarnings(False)

    gpio.setup([c['pin'] for c in chan_dict.itervalues()], gpio.OUT)

def main():
    parser = argparse.ArgumentParser(description='control a 3 color led on the gpio pins of the raspberry pi')
    parser.add_argument('method', choices=['random_transitions', 'rgb', 'fluent' ])
    parser.add_argument('--duration', default=5, type=int, help='duration used in some animations')
    parser.add_argument('--intensity', default=70, type=int, help='brightnes of the leds used in some animations')
    args = parser.parse_args()
    if args.method == '':
        args.method = 'random_transitions'
    init()
    if args.method == 'random_transitions':
        random_transitions()
    elif args.method == 'rgb':
        red_green_blue(args.duration, args.intensity)
    elif args.method == 'fluent':
        all_fluent(args.duration)
    else:
        print 'unknown method'
        sys.exit(1)

def random_transitions():
    new_rgb = {'red': 50, 'green': 50, 'blue':50}
    for c in chan_dict.itervalues():
        c['pwm'] = gpio.PWM(c['pin'], 60)
        c['pwm'].start(new_rgb[c['color']])


    steps = 100
    while(True):
        old_rgb = copy.deepcopy(new_rgb)
        # determine new rgb value to change to
        for c in new_rgb.iterkeys():
            new_rgb[c] =  random.randint(chan_dict[c]['min'], chan_dict[c]['max'])

        print old_rgb, new_rgb
        for i in range(steps):
            for c in new_rgb.iterkeys():
                step = (new_rgb[c]-old_rgb[c])/(steps*1.0)
                chan_dict[c]['pwm'].ChangeDutyCycle(old_rgb[c]+step)
            time.sleep(0.4)

def red_green_blue(duration, intensity):
    for c in chan_dict.itervalues():
        c['pwm'] = gpio.PWM(c['pin'], 100)
        c['pwm'].start(0)

    for color in itertools.imap(chan_dict.get ,itertools.cycle(chan_dict)):
        color['pwm'].ChangeDutyCycle(intensity)
        time.sleep(duration)
        color['pwm'].ChangeDutyCycle(0)

def all_fluent(duration):
    for c in chan_dict.itervalues():
        c['pwm'] = gpio.PWM(c['pin'], 100)
        c['pwm'].start(0)
    min = 10
    old = chan_dict['red']
    for color in itertools.imap(chan_dict.get ,itertools.cycle(chan_dict)):
        for i in range(25):
            color['pwm'].ChangeDutyCycle(i*2+min)
            old['pwm'].ChangeDutyCycle(50-i*2+min)
            time.sleep(0.1)
        old['pwm'].ChangeDutyCycle(0)
        old = color
        time.sleep(duration)

def control_led(color, value):
    gpio.output(chan_dict[color]['pin'], value)

if __name__  == '__main__':
    main()
