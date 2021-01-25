import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import random
import time

#27 Red RGB pin
#22 Green RGB pin
#14 Red button
#15 Green button
#4 Blue button (start)

def setup():
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    motor = RpiMotorLib.BYJMotor("GongMotor", "28BYJ")
    return motor

def light_green():
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(27, GPIO.LOW)

def light_red():
    GPIO.output(22, GPIO.LOW)
    GPIO.output(27, GPIO.HIGH)
    
def is_green_button_pressed():
    return GPIO.input(15) 
    
def is_red_button_pressed():
    return GPIO.input(14)
    
def wait(condition, motor, granularity=0.1, time_factory=time):
    end_time = time.time() + random.randint(2,5)  
    status = condition()         
    while not status and time.time() < end_time
        if is_red_button_pressed and not is_green_button_pressed:
            motor.motor_run([18, 23, 24, 25], 0.001, 64, False, "half", .05)
            #Draai motor naar rechts/clockwise
        elif is_green_button_pressed and not is_red_button_pressed:
            motor.motor_run([18, 23, 24, 25], 0.001, 64, True, "half", .05)
            #Draai motor naar links/counterclockwise
        time.sleep(granularity)
        status = condition()
    return status  

if __name__ == '__main__':
    motor = setup()
    game_over = False
    press_green_button = True
    wait_time = random.randint(2,5)
    while not game_over:
        if press_green_button: #Groene knop moet ingedrukt worden
            if wait(is_green_button_pressed, motor):
                press_green_button = not press_green_button
                light_red()
            else:
                game_over = True
                break
        else: #Rode knop moet ingedrukt worden
            if wait(is_red_button_pressed, motor):
                press_green_button = not press_green_button
                light_green()
            else:
                game_over = True
                break
    GPIO.cleanup()
            
        
