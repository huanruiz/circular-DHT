# python 3.7.1

import sys
import time
from socket import *
import threading
import os

# receive the ping command
def receive_ping_request():
	while True:
		predecessor_id, addr = serverSocket.recvfrom(1024)
		if predecessor_id:
			serverSocket.sendto(str(own_id).encode(), addr)
			print(f'A ping request message was received from Peer {predecessor_id.decode()}.')

# receive the ping response
def receive_ping_response():
	while True:
		try:
			data, (address, _) = clientSocket.recvfrom(1024)
			if data and int(data.decode()) == first_successive_id:
				print(f'A ping response message was received from Peer {first_successive_id}')
			elif data and int(data.decode()) == second_successive_id:
				print(f'A ping response message was received from Peer {second_successive_id}')	
		except OSError:
			pass

# request a file
def request_file():
	while True:
		command = input()
		command = command.split()
		if len(command) == 2 and command[0] == 'request' and command[1].isdigit():
			if int(command[1]) >= 0 and int(command[1]) < 10000:

				print('is', command[0], int(command[1]))

# initialse the peer
if len(sys.argv) == 6 and float(sys.argv[5]) >=0 and float(sys.argv[5]) <=1:
	own_id = int(sys.argv[1])
	first_successive_id = int(sys.argv[2])
	second_successive_id = int(sys.argv[3])
	MSS = float(sys.argv[4])
	drop_probability = float(sys.argv[5])
else:
	print('please input the data of correct form')
	sys.exit()

# ping client
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(3)

# ping server
serverPort = 50000 + own_id
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('127.0.0.1', serverPort))

# define the thread
thread_1 = threading.Thread(target=receive_ping_request)
thread_2 = threading.Thread(target=receive_ping_response)
thread_3 = threading.Thread(target=request_file)
thread_1.start()
thread_2.start()
thread_3.start()

time.sleep(3) # wait for initialization of the peers

# send the ping request
while True:
	clientSocket.sendto(str(own_id).encode(), ('127.0.0.1', 50000 + first_successive_id))
	clientSocket.sendto(str(own_id).encode(), ('127.0.0.1', 50000 + second_successive_id))
	time.sleep(10)

thread_3.join()
thread_2.join()
thread_1.join()