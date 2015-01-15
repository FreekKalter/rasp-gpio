import time
import uinput
import random
import copy
import itertools
import RPi.GPIO as gpio

from subprocess import call

buttons = {'up': 22, 'down':36, 'fire':32, 'left':12, 'right':18}
gpio.setup(buttons.values(), gpio.IN, pull_up_down=gpio.PUD_DOWN)



def detect_button():
    fire = 32
    jump = 36
    gpio.setup(fire, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    gpio.setup(jump, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    while(True):
        if gpio.input(fire):
            control_led('red', 1)
        else:
            control_led('red', 0)
        if gpio.input(jump):
            control_led('blue', 1)
        else:
            control_led('blue', 0)
        time.sleep(0.3)

def light_mix():
    for c in chan_dict.itervalues():
        c['pwm'] = gpio.PWM(c['pin'], 100)
        c['pwm'].start(0)
        c['current'] = 0
    color_iter = itertools.cycle(chan_dict)
    color = chan_dict[color_iter.next()]

    while(True):
        if gpio.input(buttons['up']):
            if color['current'] < 100:
                color['pwm'].ChangeDutyCycle(color['current'] + 5)
                color['current'] += 5
            print '{} {}'.format(color['color'],color['current'])
        if gpio.input(buttons['down']):
            if color['current'] > 0:
                color['pwm'].ChangeDutyCycle(color['current'] - 5)
                color['current'] -= 5
            print '{} {}'.format(color['color'],color['current'])
        if gpio.input(buttons['fire']):
            color = chan_dict[color_iter.next()]
            color['pwm'].ChangeDutyCycle(100)
            print color['color']
            time.sleep(0.2)
            color['pwm'].ChangeDutyCycle(color['current'])
        time.sleep(0.1)
        #print color

def button_test():
    while(True):
        if gpio.input(buttons['up']):
            print 'up'
            time.sleep(0.2)
        if gpio.input(buttons['down']):
            print 'down'
            time.sleep(0.2)
        if gpio.input(buttons['right']):
            print 'right'
            time.sleep(0.2)
        if gpio.input(buttons['left']):
            print 'left'
            time.sleep(0.2)
        if gpio.input(buttons['fire']):
            print 'fire'
            time.sleep(0.2)
        time.sleep(0.1)


def joystick():
    events = (uinput.BTN_JOYSTICK, uinput.ABS_X + (0, 255, 0, 0), uinput.ABS_Y + (0, 255, 0, 0))
    device = uinput.Device(events)
    # Bools to keep track of movement
    fire = False
    up = False
    down = False
    left = False
    right = False

    # Center joystick
    # syn=False to emit an "atomic" (128, 128) event.
    device.emit(uinput.ABS_X, 128, syn=False)
    device.emit(uinput.ABS_Y, 128)# Bools to keep track of movement

    while(True):
        if gpio.input(buttons['up']):
            print 'up'
            device.emit(uinput.ABS_Y, 0)
            up = True
            time.sleep(0.2)
        else:
            device.emit(uinput.ABS_Y, 128)
            up = False

        if gpio.input(buttons['down']):
            print 'down'
            device.emit(uinput.ABS_Y, 255)
            down = True
            time.sleep(0.2)
        else:
            device.emit(uinput.ABS_Y, 128)
            down = False

        if gpio.input(buttons['left']):
            print 'left'
            device.emit(uinput.ABS_X, 0)
            left = True
            time.sleep(0.2)
        else:
            device.emit(uinput.ABS_X, 128)
            left = False

        if gpio.input(buttons['right']):
            print 'right'
            device.emit(uinput.ABS_X, 255)
            right = True
            time.sleep(0.2)
        else:
            device.emit(uinput.ABS_X, 128)
            right = False

        if gpio.input(buttons['fire']):
            print 'fire'
            device.emit(uinput.BTN_JOYSTICK, 1)
            fire = True
            time.sleep(0.2)
        else:
            fire = False
            device.emit(uinput.BTN_JOYSTICK, 0)
        time.sleep(0.1)

def keyboard():
    events = {
            'up': uinput.KEY_UP,
            'down': uinput.KEY_DOWN,
            'left': uinput.KEY_LEFT,
            'right': uinput.KEY_RIGHT,
            'space': uinput.KEY_SPACE,
    }
    with uinput.Device(events.values()) as device:
        time.sleep(1)
        while True:
            if gpio.input(buttons['up']):
                device.emit_click(events['up'])
                time.sleep(0.15)
            if gpio.input(buttons['down']):
                device.emit_click(events['down'])
                time.sleep(0.15)
            if gpio.input(buttons['left']):
                device.emit_click(events['left'])
                time.sleep(0.15)
            if gpio.input(buttons['right']):
                device.emit_click(events['right'])
                time.sleep(0.15)
            if gpio.input(buttons['fire']):
                device.emit_click(events['space'])
                time.sleep(0.15)
            time.sleep(0.01)

if __name__ == '__main__':
    #red_green_blue(5, 50)
    #all_fluent(1)
    #light_mix()
    #button_test()
    #joystick()
    call(['modprobe', 'uinput'])
    keyboard()
