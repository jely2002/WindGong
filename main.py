from gpiozero import LED, Button
from RpiMotorLib import RpiMotorLib
import RPi.GPIO as GPIO

import random
import time

game_over = False
waiting_on_press = True
waiting_on_release = False
press_green_button = True


# 27 Red RGB pin
# 22 Green RGB pin
# 14 Red button
# 15 Green button
# 4 Blue button (start)

def setup_motor():
    stepper = RpiMotorLib.BYJMotor("motor", "28BYJ")
    return stepper


def light_green(red, green):
    red.off()
    green.on()


def light_red(red, green):
    red.on()
    green.off()


def stop_game(red, green):
    red.off()
    green.off()
    GPIO.cleanup()


def green_activated():
    global waiting_on_press
    global game_over
    if waiting_on_press and press_green_button:
        waiting_on_press = not waiting_on_press
    elif not press_green_button:
        game_over = True


def green_held(stepper):
    global waiting_on_release
    if waiting_on_release and press_green_button:
        stepper.motor_run([18, 23, 24, 25], .01, 100, False, False, "half", .05)


def red_activated():
    global waiting_on_press
    global game_over
    if waiting_on_press and not press_green_button:
        waiting_on_press = not waiting_on_press
    elif press_green_button:
        game_over = True


def red_held(stepper):
    global waiting_on_release
    if waiting_on_release and not press_green_button:
        stepper.motor_run([18, 23, 24, 25], .01, 100, False, False, "half", .05)


if __name__ == '__main__':
    red_led = LED(27)
    green_led = LED(22)
    red_button = Button(14)
    green_button = Button(15)
    blue_button = Button(4)
    motor = setup_motor()

    green_button.when_activated(green_activated())
    green_button.when_held(green_held(motor))
    red_button.when_activated(red_activated())
    red_button.when_held(red_held(motor))

    global waiting_on_release
    global waiting_on_press
    global game_over
    global press_green_button

    while not game_over:
        if press_green_button:
            waiting_on_press = True
            green_button.wait_for_active(1)
            if waiting_on_press or game_over:
                break
            waiting_on_release = True
            time.sleep(random.randint(2, 5))
            light_red(red_led, green_led)
            waiting_on_release = False
            press_green_button = False
        else:
            waiting_on_press = True
            red_button.wait_for_active(1)
            if waiting_on_press or game_over:
                break
            waiting_on_release = True
            time.sleep(random.randint(2, 5))
            light_green(red_led, green_led)
            waiting_on_release = False
            press_green_button = True
    stop_game(red_led, green_led)
