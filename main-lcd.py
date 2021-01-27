from gpiozero import LED, Button
import datetime
import random
import time
import lcd_driver

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

motor_a1 = LED(18) #18
motor_a2 = LED(23) #23
motor_b1 = LED(24) #24
motor_b2 = LED(25) #25

lcd = lcd_driver.lcd()

red_led = LED(27) #27
green_led = LED(22) #22

blue_button = Button(4) #4
red_button = Button(14) #14
green_button = Button(15) # 15


def turn_motor(clockwise):
    global step_index
    if step_index >= 4:
        step_index = 0
    if clockwise:
        print("Clockwise")
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
        print("Counterclockwise")
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
    global motor_a1, motor_a2, motor_b1, motor_b2
    motor_a1.value = w1
    motor_a2.value = w2
    motor_b1.value = w3
    motor_b2.value = w4


def red_pressed():
    global state, game_over, spin_motor, turn_clockwise
    if state == "press_red":
        state = "wait_random"
    elif state == "wait_random" and not green_led_on:
        spin_motor = True
        turn_clockwise = False
    elif switch_time is not None and (datetime.datetime.now() - switch_time).total_seconds() > 0.5:
        game_over = True


def green_pressed():
    global state, game_over, spin_motor, turn_clockwise
    if state == "press_green":
        state = "wait_random"
    elif state == "wait_random" and green_led_on:
        spin_motor = True
        turn_clockwise = True
    elif switch_time is not None and (datetime.datetime.now() - switch_time).total_seconds() > 0.5:
        game_over = True


def red_released():
    global state, spin_motor
    if state == "wait_random" and not green_led_on:
        spin_motor = False


def green_released():
    global state, spin_motor
    if state == "wait_random" and green_led_on:
        spin_motor = False


def update_led():
    global red_led, green_led
    if green_led_on:
        red_led.off()
        green_led.on()
        print("green on")
    else:
        green_led.off()
        red_led.on()
        print("red on")


lcd.lcd_display_string("Press the blue", 1)
lcd.lcd_display_string("button to start!", 2)

blue_button.wait_for_press()

lcd.lcd_clear()
lcd.lcd_display_string("3", 1)

time.sleep(1)

lcd.lcd_clear()
lcd.lcd_display_string("2", 1)

time.sleep(1)

lcd.lcd_clear()
lcd.lcd_display_string("1", 1)

time.sleep(1)

red_button.when_pressed = red_pressed
green_button.when_pressed = green_pressed
red_button.when_released = red_released
green_button.when_released = green_released

update_led()


while not game_over:
    if state == "press_green" or state == "press_red":
        lcd.lcd_clear()
        if state == "press_green":
            lcd.lcd_display_string("Press the", 1)
            lcd.lcd_display_string("green button!", 2)
        else:
            lcd.lcd_display_string("Press the", 1)
            lcd.lcd_display_string("red button!", 2)
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
    time.sleep(0.01)

print("Game over!")
red_led.off()
green_led.off()

lcd.lcd_clear()
lcd.lcd_display_string("Game over!", 1)

time.sleep(5)

lcd.lcd_clear()
