#calibrate servo
import RPi.GPIO as GPIO
import time

# Set the GPIO mode and pin number
GPIO.setmode(GPIO.BCM)
servo_pin = 12

# Set up the PWM pin
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # PWM frequency of 50Hz (standard for servos)
	
# Function to set the servo angle
def set_servo_angle(angle):
    duty_cycle = 2 + (angle / 18)  # Map angle (0-180) to duty cycle (2-12)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(2.3)  # Give the servo time to move

# Example usage: rotate the servo to 0 degrees, then to 90 degrees, and finally to 180 degrees
try:
    pwm.start(2.5)  # Start PWM with a duty cycle of 0 (servo at 0 degrees)
    while True:
        set_servo_angle(0)
        set_servo_angle(90)
        set_servo_angle(180)
        time.sleep(1)
        print('180')

except KeyboardInterrupt:
    # Clean up the GPIO settings
    pwm.stop()
    GPIO.cleanup()
