import RPi.GPIO as gpio
import time
import argparse
import copy
import random
import sys
import itertools


class LedControl:

    def __init__(self):
        gpio.setmode(gpio.BOARD)
        gpio.setwarnings(False)
        self.chan_dict = {'red': {'color': 'red', 'pin': 7, 'max': 100, 'min': 40},
                          'blue': {'color': 'blue', 'pin': 11, 'max': 80, 'min': 30},
                          'green': {'color': 'green', 'pin': 16, 'max': 100, 'min': 40}}
        gpio.setup([c['pin'] for c in self.chan_dict.itervalues()], gpio.OUT)

    def random_transitions(self):
        new_rgb = {'red': 50, 'green': 50, 'blue': 50}
        for c in self.chan_dict.itervalues():
            c['pwm'] = gpio.PWM(c['pin'], 60)
            c['pwm'].start(new_rgb[c['color']])

        steps = 100
        while(True):
            old_rgb = copy.deepcopy(new_rgb)
            # determine new rgb value to change to
            for c in new_rgb.iterkeys():
                new_rgb[c] = random.randint(self.chan_dict[c]['min'], self.chan_dict[c]['max'])

            print old_rgb, new_rgb
            for i in range(steps):
                for c in new_rgb.iterkeys():
                    step = (new_rgb[c] - old_rgb[c]) / (steps * 1.0)
                    self.chan_dict[c]['pwm'].ChangeDutyCycle(old_rgb[c] + step)
                time.sleep(0.4)

    def red_green_blue(self, duration, intensity):
        for c in self.chan_dict.itervalues():
            c['pwm'] = gpio.PWM(c['pin'], 100)
            c['pwm'].start(0)

        for color in itertools.imap(self.chan_dict.get, itertools.cycle(self.chan_dict)):
            color['pwm'].ChangeDutyCycle(intensity)
            time.sleep(duration)
            color['pwm'].ChangeDutyCycle(0)

    def all_fluent(self, duration):
        for c in self.chan_dict.itervalues():
            c['pwm'] = gpio.PWM(c['pin'], 100)
            c['pwm'].start(0)
        min = 10
        old = self.chan_dict['red']
        for color in itertools.imap(self.chan_dict.get, itertools.cycle(self.chan_dict)):
            for i in range(25):
                color['pwm'].ChangeDutyCycle(i * 2 + min)
                old['pwm'].ChangeDutyCycle(50 - i * 2 + min)
                time.sleep(0.1)
            old['pwm'].ChangeDutyCycle(0)
            old = color
            time.sleep(duration)

    def control_led(self, color, value):
        gpio.output(self.chan_dict[color]['pin'], value)


def main():
    parser = argparse.ArgumentParser(
        description='control a 3 color led on the gpio pins of the raspberry pi')
    parser.add_argument('method', choices=['random_transitions', 'rgb', 'fluent'])
    parser.add_argument('--duration', default=5, type=int, help='duration used in some animations')
    parser.add_argument('--intensity', default=70, type=int,
                        help='brightnes of the leds used in some animations')
    args = parser.parse_args()
    if args.method == '':
        args.method = 'random_transitions'
    lc = LedControl()
    if args.method == 'random_transitions':
        lc.random_transitions()
    elif args.method == 'rgb':
        lc.red_green_blue(args.duration, args.intensity)
    elif args.method == 'fluent':
        lc.all_fluent(args.duration)
    else:
        print 'unknown method'
        sys.exit(1)


if __name__ == '__main__':
    main()
