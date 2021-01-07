import asyncio
import websockets

class client:
	ws=None
	def __init__(self):
		print("Client Connected")
		self.ws=None

	async def on_recieve(self,websocket,path):
		self.ws=websocket
		while True:
			data= await self.ws.recv()
			print(data)
	async def on_send(self,data):
		await self.ws.send(data)