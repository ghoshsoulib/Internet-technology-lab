import asyncio
import websockets

class Client:
	def __init__(self, a):
		self.name = a
		self.dct = {'role':'guest'}

clients = {}

async def hello(websocket, path):
	while True:
		x = await websocket.recv()
		if x in clients:
			await websocket.send('duplicate user name')
		else:
			await websocket.send('success')
			print('Connected to '+x)
			break
	c = Client(x)
	clients[x] = c

	# async for data in websocket:
	while True:
		data = await websocket.recv()
		arr = data.split()
		
		if arr[0] == 'q':
			await websocket.send('exiting')
			break
		
		elif arr[0] == 'put': 
			if len(arr) == 3:
				c.dct[arr[1]] = arr[2]
				await websocket.send('done')
			else:
				await websocket.send('wrong message format')

		elif arr[0] == 'get':
			if len(arr) == 2:
				if arr[1] in c.dct:
					await websocket.send(c.dct[arr[1]])
				else:
					await websocket.send('key not found')

			elif len(arr) == 3:
				if c.dct['role'] == 'guest':
					await websocket.send('you are not allowed to access keys of other users'.encode('utf-8'))
				elif arr[1] in clients:
					c2 = clients[arr[1]]
					if arr[2] in c2.dct:
						await websocket.send(c2.dct[arr[2]])
					else:
						await websocket.send('key not found')
				else:
					await websocket.send('user not found')

			else:
				await websocket.send('wrong message format')

		elif arr[0] == 'upgrade':
			if c.dct['role'] == 'guest':
				c.dct['role'] = 'manager'
				await websocket.send('upgraded to manager')
			else:
				await websocket.send('already a manager')

		else:
			await websocket.send('wrong message format')

	del clients[c.name]

addr = ""
port = 1603
start_server = websockets.server.serve(hello, addr, port, ping_interval = 1000, ping_timeout = 1000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()