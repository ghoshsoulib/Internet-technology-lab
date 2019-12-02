import asyncio
import websockets

addr = str(input('>>Enter ip address : '))
port = int(input('>>Enter port address : '))

cmds = ['get','put','upgrade','q']
num_cmd = 4

async def hello():
	uri = "ws://"+addr+":"+str(port)
	async with websockets.connect(uri) as websocket:

		while True:
			if not websocket.open:
				print("Websocket not open. Trying to reconnect")
				websocket = await websockets.connect(uri)
			user = str(input('>>Enter user name : '))
			await websocket.send(user)
			ans = await websocket.recv()
			if ans == 'success':
				print('user created')
				break
			else:
				print(str(ans))

		while True:
			if not websocket.open:
				print("Websocket not open. Trying to reconnect")
				websocket = await websockets.connect(uri)
			x = str(input(">>"))
			words = x.split()
			for i in range(len(words)):
				if words[i] in cmds:
					x=words[i]
					if x == 'upgrade' or x=='q':
						await websocket.send(x)
						x2 = await websocket.recv()
						print(str(x2))
						if x=='q':
							break
				elif (i==len(words)-1) or (words[i+1] in cmds):
					x=x+' '+words[i]
					boo=False
					for j in range(num_cmd):
						boo = boo or x.startswith(cmds[j])
					if boo:
						await websocket.send(x)
						x2 = await websocket.recv()
						print(str(x2))
					else:
						print('wrong message format')
				else:
					x=x+' '+words[i]
			if x=='q':
				break

asyncio.get_event_loop().run_until_complete(hello())