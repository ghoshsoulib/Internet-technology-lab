import socket

cmds = ['get','put','upgrade','q']
num_cmd = 3

addr = str(input('Enter ip address : '))
port = int(input('Enter port address : '))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((addr,port))


while True:
	user = str(input('Enter user name : '))
	s.send(user.encode('utf-8'))
	ans = s.recv(1024).decode()
	if ans == 'success':
		break
	else:
		print(ans)

while True:
	x = str(input())
	words = x.split()
	for i in range(len(words)):
		if words[i] in cmds:
			x=words[i]
			if x == 'upgrade' or x=='q':
				s.send(x.encode('utf-8'))
				x2 = s.recv(1024).decode()
				print(x2)
				if x=='q':
					break
		elif (i==len(words)-1) or (words[i+1] in cmds):
			x=x+' '+words[i]
			boo=False
			for j in range(num_cmd):
				boo = boo or x.startswith(cmds[j])
			if boo:
				s.send(x.encode('utf-8'))
				x2 = s.recv(1024).decode()
				print(x2)
			else:
				print('wrong message format')
		else:
			x=x+' '+words[i]
	if x=='q':
		break
