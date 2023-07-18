import socket
from gpiozero import Button, LED

# IP address and port of the second Raspberry Pi
HOST = ''
PORT = 5000

# Creating a button and LED objects
button = Button(4)  
led1 = LED(26)  # LED 1 connected to BCM pin 26
led2 = LED(19)  # LED 2 connected to BCM pin 19

# Socket communication setup
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

# Accepting the connection from the first Raspberry Pi
conn, addr = sock.accept()
print('Connected to', addr)

try:
    while True:
        button.wait_for_press()
        led1.on()  # Turn on LED 1
        led2.on()  # Turn on LED 2
        conn.sendall(b'start')  # Sending 'start' command to the first Raspberry Pi
        button.wait_for_release()
        led1.off()  # Turn off LED 1
        led2.on()  # Turn off LED 2
        conn.sendall(b'stop')  # Sending a 'stop' command to the first Raspberry Pi
        

except KeyboardInterrupt:
    GPIO.cleanup()

conn.sendall(b'exit')  # Sending 'exit' command to the first Raspberry Pi
conn.close()
sock.close()

