import socket
import json


# This functions sends a message to the receiver
# The parameters of this function are conn: which
# is a socket object and msg which is a string that
# is sent to the sender.

def send_msg(conn, msg):
	serialized = json.dumps(msg).encode('utf-8')
	length = str(len(serialized)) + '\n'
	length = length.encode('utf-8')
	conn.send(length)
	conn.sendall(serialized)


# Try to define a socket
try:
	s = socket.socket()
	print("Socket Created")
except socket.error as err:
	print("Socket Creation Failed with Error :: ", err)


# Define the port Number on which
# the receiver listens
RECEVER_PORT = 1234

# Define the IP address of the receiver
RECEVER_IP = "192.168.1.252"

# Connect the sender to the receiver
s.connect((RECEVER_IP, RECEVER_PORT))

# Send a message to the sender
send_msg(s, "Hello World!")
print("Message Sent!")
s.close()



