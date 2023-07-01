import socket
import json


import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
servo_pin = 12

# Set up the PWM pin
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # PWM frequency of 50Hz (standard for servos)
duty_cycle = 2 + (0 / 18)  # Map angle (0-180) to duty cycle (2-12)
pwm.ChangeDutyCycle(duty_cycle)

reference_angle = 90
# Function to set the servo angle

def set_relative_servo_angle(ref_angle, angle):
    # Calculate the new angle relative to the reference angle
    new_angle = ref_angle + angle
    new_angle = max(0, min(180, new_angle))  # Ensure the angle is between 0 and 180
    
    # Convert the angle to duty cycle
    duty_cycle = 2 + (new_angle / 18)  # Map angle (0-180) to duty cycle (2-12)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.38)  # Give the servo time to move
    return new_angle


pwm.start(2.5)
def receive_coordinates():
    global reference_angle
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define the server address and port
    server_address = '192.168.148.234'
    server_port = 12345

    # Connect to the server
    client_socket.connect((server_address, server_port))
    print('Connected to the server.')
    
    try:
        while True:
            # Receive data from the server
            data = client_socket.recv(1024)

            if not data:
                break

            # Decode the received data
            received_json = data.decode()

            # Parse the JSON data
            try:
                coordinates = json.loads(received_json)
                center_x = float(coordinates['center_x'])
                center_y = float(coordinates['center_y'])
                #pwm.start(2.5)
               
                print(reference_angle)
                # Process the received coordinates
                process_coordinates(center_x, center_y)

                if center_x < 350:
                   #reference_angle = set_relative_servo_angle(reference_angle, 3)
                   #reference_angle = set_relative_servo_angle(reference_angle, 5)
                   #reference_angle = set_relative_servo_angle(reference_angle, 7)
                   #reference_angle = set_relative_servo_angle(reference_angle, 11)
                   reference_angle = set_relative_servo_angle(reference_angle, 15)
                   
                  #set_relative_servo_angle(reference_angle, 15)
                   #set_relative_servo_angle(reference_angle, 25)
                   #set_relative_servo_angle(reference_angle, 30)
                if center_x > 550:
                   #reference_angle = set_relative_servo_angle(reference_angle, -3)
                   #reference_angle = set_relative_servo_angle(reference_angle, -5)
                   #reference_angle = set_relative_servo_angle(reference_angle, -7)
                   #reference_angle = set_relative_servo_angle(reference_angle, -11)
                   reference_angle = set_relative_servo_angle(reference_angle, -15)
                   #set_relative_servo_angle(reference_angle, -15)
                   #set_relative_servo_angle(reference_angle, -25)
                #  set_relative_servo_angle(reference_angle, -35)
                #  set_relative_servo_angle(reference_angle, 40)
                
            except json.JSONDecodeError:
                   print('Error parsing JSON:', received_json)

    finally:
        # Close the client socket
        client_socket.close()
        print('Connection closed.')

def process_coordinates(center_x, center_y):
    # Process the received coordinates here
    print('Received coordinates: Center X =', center_x, 'Center Y =', center_y)

# Start receiving coordinates
receive_coordinates()

