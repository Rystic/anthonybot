#!/usr/bin/env python
import socket
import pifacedigitalio

from decimal import *

HOST = ''
PORT = 50010
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
while 1:
	conn, addr = s.accept()
	print('Connected by', addr)
	pfd = pifacedigitalio.PiFaceDigital()
	while 1:
		data = conn.recv(1024)
		if not data: break
		decoded_data = data.decode('unicode-escape')
		decoded_data = decoded_data.partition(",")
		if (decoded_data[0] == "joystick"):
			coords = decoded_data[2].split()
			coords[0] = Decimal(coords[0].encode('utf-8'))
			coordAndOverFlow = coords[1].partition('!')
			coords[1] = Decimal(coordAndOverFlow[0])
			if (coords[0] == 0 and coords[1] == 1):
				pfd.output_pins[0].value = 0
				pfd.output_pins[1].value = 0
				pfd.output_pins[2].value = 1
				pfd.output_pins[4].value = 1
			elif (coords[0] == 1 and coords[1] == 0):
				pfd.output_pins[0].value = 1
				pfd.output_pins[1].value = 0
				pfd.output_pins[2].value = 0
				pfd.output_pins[4].value = 1
			elif (coords[0] == 0 and coords[1] == -1):
				pfd.output_pins[0].value = 1
				pfd.output_pins[1].value = 1
				pfd.output_pins[2].value = 0
				pfd.output_pins[4].value = 0
			elif (coords[0] == -1 and coords[1] == 0):
				pfd.output_pins[0].value = 0
				pfd.output_pins[1].value = 1
				pfd.output_pins[2].value = 1
				pfd.output_pins[4].value = 0
			elif (coords[0] == 0 and coords[1] == 0):
				pfd.output_pins[0].value = 0
				pfd.output_pins[1].value = 0
				pfd.output_pins[2].value = 0
				pfd.output_pins[4].value = 0

		elif (decoded_data[0] == "a_button"):
			pfd.output_pins[7].value = 1
		elif (decoded_data[0] == "a_button_off"):
			pfd.output_pins[7].value = 0
		elif (decoded_data[0] == "b_button"):
			break
	print("finish")
	pfd.output_pins[0].value = 0
	pfd.output_pins[1].value = 0
	pfd.output_pins[2].value = 0
	pfd.output_pins[4].value = 0
	pfd.output_pins[7].value = 0
	conn.close()
	s.close()
