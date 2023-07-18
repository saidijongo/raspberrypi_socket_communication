import RPi.GPIO as GPIO
import time
import socket

# Defining pins
CW_PIN = 38   # CW+ pin
CCW_PIN = 36  # CCW+ pin
LEFT_SENSOR_PIN = 40  # Left photomicrosensor pin
RIGHT_SENSOR_PIN = 32 # Right photomicrosensor pin

# Define the delay for smooth rotation
DELAY = 0.009

# Set up the GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(CW_PIN, GPIO.OUT)
GPIO.setup(CCW_PIN, GPIO.OUT)
GPIO.setup(LEFT_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to rotate the motor 360 degrees
def rotate_360(direction_pin):
    angle = 0
    for _ in range(500):  # 500 steps for 360 degrees
        GPIO.output(direction_pin, GPIO.HIGH)
        time.sleep(DELAY)
        GPIO.output(direction_pin, GPIO.LOW)
        time.sleep(DELAY)
        angle += 0.72  # Increment angle by 0.72 degrees per step
        print("Current angle: {:.2f} degrees".format(angle))


def stop():
    GPIO.output(CW_PIN, GPIO.LOW)
    GPIO.output(CCW_PIN, GPIO.LOW)

# Socket communication setup
HOST = '172.16.100.171'  # IP address of the first Raspberry Pi
PORT = 5000  

# Connect to the second Raspberry Pi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

try:
    while True:
        data = sock.recv(1024).decode()  # Receive data from the second Raspberry Pi

        # Check the received data
        if data == 'start':
            # Rotate clockwise until interrupted by the right photomicrosensor
            while GPIO.input(RIGHT_SENSOR_PIN) == GPIO.HIGH:
                print("Rotating clockwise")
                rotate_360(CW_PIN)
           
            # Stop the motor for 3 seconds
            stop()
            time.sleep(3)
           
            # Rotate counter clockwise until interrupted by the left photomicrosensor
            while GPIO.input(LEFT_SENSOR_PIN) == GPIO.HIGH:
                print("Rotating counter clockwise")
                rotate_360(CCW_PIN)
               
        elif data == 'stop':
            # Stop the motor
            stop()
           
        elif data == 'exit':
            # Exit the loop
            break

except KeyboardInterrupt:
    pass

sock.close()
GPIO.cleanup()