import time
import uinput
import argparse
import RPi.GPIO as gpio
from subprocess import call


class Joystick():

    def __init__(self):
        try:
            call(['modprobe', 'uinput'])
        except Exception as e:
            print e
        self.buttons = {'up': 22, 'down': 36, 'fire': 32, 'left': 12, 'right': 18}
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.buttons.values(), gpio.IN, pull_up_down=gpio.PUD_DOWN)

    def joystick(self):
        events = (uinput.BTN_JOYSTICK, uinput.ABS_X + (0, 255, 0, 0), uinput.ABS_Y + (0, 255, 0, 0))
        device = uinput.Device(events)
        # Center joystick
        # syn=False to emit an "atomic" (128, 128) event.
        device.emit(uinput.ABS_X, 128, syn=False)
        device.emit(uinput.ABS_Y, 128)  # Bools to keep track of movement

        while(True):
            if gpio.input(self.buttons['up']):
                print 'up'
                device.emit(uinput.ABS_Y, 0)
                time.sleep(0.2)
            else:
                device.emit(uinput.ABS_Y, 128)

            if gpio.input(self.buttons['down']):
                print 'down'
                device.emit(uinput.ABS_Y, 255)
                time.sleep(0.2)
            else:
                device.emit(uinput.ABS_Y, 128)

            if gpio.input(self.buttons['left']):
                print 'left'
                device.emit(uinput.ABS_X, 0)
                time.sleep(0.2)
            else:
                device.emit(uinput.ABS_X, 128)

            if gpio.input(self.buttons['right']):
                print 'right'
                device.emit(uinput.ABS_X, 255)
                time.sleep(0.2)
            else:
                device.emit(uinput.ABS_X, 128)

            if gpio.input(self.buttons['fire']):
                print 'fire'
                device.emit(uinput.BTN_JOYSTICK, 1)
                time.sleep(0.2)
            else:
                device.emit(uinput.BTN_JOYSTICK, 0)
            time.sleep(0.1)

    def keyboard(self):
        print 'in keyboard func'
        events = {'up': uinput.KEY_UP,
                  'down': uinput.KEY_DOWN,
                  'left': uinput.KEY_LEFT,
                  'right': uinput.KEY_RIGHT,
                  'space': uinput.KEY_SPACE}
        with uinput.Device(events.values()) as device:
            time.sleep(1)
            while True:
                if gpio.input(self.buttons['up']):
                    device.emit_click(events['up'])
                    time.sleep(0.15)
                if gpio.input(self.buttons['down']):
                    device.emit_click(events['down'])
                    time.sleep(0.15)
                if gpio.input(self.buttons['left']):
                    device.emit_click(events['left'])
                    time.sleep(0.15)
                if gpio.input(self.buttons['right']):
                    device.emit_click(events['right'])
                    time.sleep(0.15)
                if gpio.input(self.buttons['fire']):
                    device.emit_click(events['space'])
                    time.sleep(0.15)
                time.sleep(0.01)


def main():
    parser = argparse.ArgumentParser(
        description='"device driver" for the commodore joystick connected to the gpio pins')
    parser.add_argument('method', choices=['keyboard', 'joystick'])
    args = parser.parse_args()
    j = Joystick()
    if args.method == 'keyboard':
        j.keyboard()
    elif args.method == 'joystick':
        j.joystick()


if __name__ == '__main__':
    main()
