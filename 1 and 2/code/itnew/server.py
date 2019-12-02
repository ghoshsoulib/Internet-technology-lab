import socket
from _thread import *
import threading

srvr_lock = threading.Lock()

class Client:
	def __init__(self, a, c):
		self.name = a
		self.conn = c
		self.dct = {'role':'guest'}

clients = {}

def operate(c):
	while True:
		data = c.conn.recv(1024).decode()
		arr = data.split()
		
		if arr[0] == 'q':
			c.conn.send('exiting'.encode('utf-8'))
			break
		
		elif arr[0] == 'put': 
			if len(arr) == 3:
				c.dct[arr[1]] = arr[2]
				c.conn.send('done'.encode('utf-8'))
			else:
				c.conn.send('wrong message format'.encode('utf-8'))

		elif arr[0] == 'get':
			if len(arr) == 2:
				if arr[1] in c.dct:
					c.conn.send(c.dct[arr[1]].encode('utf-8'))
				else:
					c.conn.send('key not found'.encode('utf-8'))

			elif len(arr) == 3:
				if c.dct['role'] == 'guest':
					c.conn.send('you are not allowed to access keys of other users'.encode('utf-8'))
				elif arr[1] in clients:
					c2 = clients[arr[1]]
					if arr[2] in c2.dct:
						c.conn.send(c2.dct[arr[2]].encode('utf-8'))
					else:
						c.conn.send('key not found'.encode('utf-8'))
				else:
					c.conn.send('user not found'.encode('utf-8'))

			else:
				c.conn.send('wrong message format'.encode('utf-8'))

		elif arr[0] == 'upgrade':
			if c.dct['role'] == 'guest':
				c.dct['role'] = 'manager'
				c.conn.send('upgraded to manager'.encode('utf-8'))
			else:
				c.conn.send('already a manager'.encode('utf-8'))

		else:
			c.conn.send('wrong message format'.encode('utf-8'))

	c.conn.close()
	del clients[c.name]


def main():
	addr = "127.0.0.1"
	port = 1601
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((addr,port))
	s.listen(5)

	while True:
		c, addr2 = s.accept()
		while True:
			x = c.recv(1024).decode()
			if x in clients:
				c.send('duplicate user name'.encode('utf-8'))
			else:
				c.send('success'.encode('utf-8'))
				print('Connected to '+x+':'+str(addr2))
				break
		cc = Client(x,c)
		clients[x] = cc
		# srvr_lock.acquire()
		start_new_thread(operate, (cc,))
	
	s.close()

if __name__ == '__main__':
	main()
