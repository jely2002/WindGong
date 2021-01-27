from gpiozero import LED, Button
import datetime
import random
import time

state = "press_green"
game_over = False
green_led_on = True
change_time = None
start_time = None
switch_time = None
random_seconds = None
spin_motor = False
turn_clockwise = True
step_index = 0
#PIN_A1 = LED(18)
#PIN_A2 = LED(16)
#PIN_B1 = LED(24)
#PIN_B2 = LED(14)

red_button = Button(22)
green_button = Button(23)


def turn_motor(clockwise):
    global step_index
    if step_index >= 4:
        step_index = 0
    if clockwise:
        print("clockwise")
        if step_index == 0:
            set_step(1, 0, 1, 0)
        elif step_index == 1:
            set_step(0, 1, 1, 0)
        elif step_index == 2:
            set_step(0, 1, 0, 1)
        elif step_index == 3:
            set_step(1, 0, 0, 1)
        step_index += 1
    else:
        print("counterclockwise")
        if step_index == 0:
            set_step(1, 0, 0, 1)
        elif step_index == 1:
            set_step(0, 1, 0, 1)
        elif step_index == 2:
            set_step(0, 1, 1, 0)
        elif step_index == 3:
            set_step(1, 0, 1, 0)
        step_index += 1


def set_step(w1, w2, w3, w4):
    pass
    #global PIN_A1, PIN_A2, PIN_B2, PIN_B1
    #PIN_A1.value = w1
    #PIN_A2.value = w2
    #PIN_B1.value = w3
    #PIN_B2.value = w4


def red_pressed():
    global state
    global game_over
    global spin_motor
    global turn_clockwise
    if state == "press_red":
        state = "wait_random"
    elif state == "wait_random" and not green_led_on:
        spin_motor = True
        turn_clockwise = False
    elif switch_time is not None and (datetime.datetime.now() - switch_time).total_seconds() > 0.5:
        game_over = True


def green_pressed():
    global state
    global game_over
    global spin_motor
    global turn_clockwise
    if state == "press_green":
        state = "wait_random"
    elif state == "wait_random" and green_led_on:
        spin_motor = True
        turn_clockwise = True
    elif switch_time is not None and (datetime.datetime.now() - switch_time).total_seconds() > 0.5:
        game_over = True


def red_released():
    global state
    global spin_motor
    if state == "wait_random" and not green_led_on:
        spin_motor = False


def green_released():
    global state
    global spin_motor
    if state == "wait_random" and green_led_on:
        spin_motor = False


def update_led():
    if green_led_on:
        print("green on")
    else:
        print("red on")

print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)
print("go")
red_button.when_pressed = red_pressed
green_button.when_pressed = green_pressed
red_button.when_released = red_released
green_button.when_released = green_released



update_led()


while not game_over:
    if state == "press_green" or state == "press_red":
        start_time = None
        random_seconds = None
        if change_time is None:
            change_time = datetime.datetime.now()
        if (datetime.datetime.now() - change_time).total_seconds() > 1:
            game_over = True
            break
    elif state == "wait_random":
        if spin_motor:
            turn_motor(turn_clockwise)
        change_time = None
        if random_seconds is None:
            random_seconds = random.randint(2, 5)
        if start_time is None:
            start_time = datetime.datetime.now()
        if (datetime.datetime.now() - start_time).total_seconds() > random_seconds:
            green_led_on = not green_led_on
            update_led()
            switch_time = datetime.datetime.now()
            if green_led_on:
                state = "press_green"
            else:
                state = "press_red"
    time.sleep(0.005)

print("Game over!")
