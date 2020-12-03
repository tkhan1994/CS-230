import socket
import json

# This function returns a string 
# which contains the messages sent
# by the sender. The protocol is 
# that a message ends with a new line 
# character "\n"
def get_message(conn):
	length_str = b''
	char = conn.recv(1)
	while char != b'\n':
		length_str += char
		char = conn.recv(1)
	total = int(length_str)
	off = 0
	msg = b''
	while off < total:
		temp = conn.recv(total - off)
		off = off + len(temp)
		msg = msg + temp
	return json.loads(msg.decode('utf-8'))


# Try to define a socket
try:
	s = socket.socket()
	print("Socket Created")
except socket.error as err:
	print("Socket Creation Failed with Error :: ", err)


# Define the port on which the receiver
# will listen to receiver requests
port = 1234

# The host refers to the local IP Address of
# my computer.
host = socket.gethostbyname(socket.gethostname())


# Bind the socket and host on
# which the receiver will accept
# incoming connections
s.bind((host, port))


# Make the recevr listen on the specified
# IP Address and port number for connection
# requests from the sender
s.listen(0)
print("Host ", host, " is listening on ", port)

try:
	while True:
			# conn is a socket new object used for
			# communication between the sender and
			# the receiver. addr is the IP address
			# of the sender.
			conn, addr = s.accept()
			print("Got connection form ", addr)
			message = get_message(conn)
			print("Message from Sender :: ", message)

# A keyboard Interrupt (ctrl + c) ends the socket
except KeyboardInterrupt:
	print("Socket Closed!")
	s.close()
