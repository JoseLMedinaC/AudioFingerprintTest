# -*- coding: utf-8 -*-
import socket
import tempfile
import os, sys
import subprocess 
import sys
import time
import numpy as np
'''
This script conects to a server in order to retrive information about a audio sample 
Audio sample name for this example is input.wav
The server is listening at 190.15.132.90 port 9050
'''
def connectserver(file,puerto):
		server_address =('190.15.132.90', puerto)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(server_address) #connect to server
		size=int(os.stat(file).st_size)
		sock.send(str(size))		
		if 'OK' not in  str(sock.recv(1024)):
			print('No OK')
			return 0
		name,ext=os.path.splitext(file)
		sock.send(ext)
		if  'OK' not in  str(sock.recv(1024)):
			return 0
		quality='low'
		sock.send(quality)
		if  'OK' not in  str(sock.recv(1024)):
			return 0
		f = open(file,'rb') #open in binary
		l = f.read(1024)
		while(l):		#send file
			sock.send(l)
			l=f.read(1024)	
		respuesta=sock.recv(2048) #reseve a response from server		
		sock.close
		if 'message' in respuesta: #there is no audio wich match with the sample 
			print respuesta
			return 0
		else:
			import json
			datosjson=json.loads(str(respuesta)) #load data as json
			vectors=[] 
			for key,value in datosjson.iteritems():
				vectors.append(str(key)) 	#vectors load all candidates retriving by server
			if len(vectors)>1:
				for vector in vectors: # rank and print all candidates 
					print vector[0]
					nombre=datosjson[vector[0]][0][1]
					print(nombre) # print the name of a candidate
			else:
					print(datosjson['vector0'][0][1]) #print the result
			return 1

if __name__=='__main__':
	file='salida.wav'		#file name
	result=connectserver(file,9050)									
	print('Termino')
