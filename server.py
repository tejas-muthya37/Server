import asyncio
import websockets
import sqlite3
import json
from client import *
from atm import *
from Crypto.Random import get_random_bytes
import base64

# with open('easyBuy.json', 'w') as file:
    # json.dump(cart1, file)

    # with open('easyBuy.json') as file:
    # cart1 = json.load(file)

def load_json(data):
	return json.loads(data)
def register_user(data):
	user=load_json(data)
	key = get_random_bytes(32)
	key = base64.b32encode(key)	
	print(key)
	user["secretkey"]=key
	return user
file="""
{ 
  "fname": "John",
  "lname": "John",
  "birthdate": "1999-01-19",
  "housenumber": 30,
  "streetname": "New York",
  "locality": "sadas",
  "pincode": 111111,
  "phonenumber": "111111111",
  "email": "xyz@gmail.com"
}
"""
print(file)
user=register_user(file)

connection = sqlite3.connect("bank.db")

string1 = "TEJAS"

crsr = connection.cursor()

create_table = """ CREATE TABLE IF NOT EXISTS bank (
	
	fname VARCHAR(20),
	lname VARCHAR(30),
	birthdate DATE,
	housenumber VARCHAR(10),
	streetname VARCHAR(10),
	locality VARCHAR(20),
	pincode INTEGER,
	phonenumber BIGINT,
	email VARCHAR(30),
	-- password
	secretkey VARCHAR(64)
	

); """

crsr.execute(create_table)

insert_data = """ INSERT INTO bank VALUES (
	
	\""""+user["fname"]+"""\",
	\""""+user["lname"]+"""\",
	\""""+user["birthdate"]+"""\",
	\""""+str(user["housenumber"])+"""\",
	\""""+user["streetname"]+"""\",
	\""""+user["locality"]+"""\",
	\""""+str(user["pincode"])+"""\",
	"""+str(user["phonenumber"])+""",
	\""""+user["email"]+"""\",
	\""""+str(user["secretkey"])+"""\"
	);
	"""
print (insert_data)
crsr.execute(insert_data)

connection.commit()

clients={}
atm=[]


# class atm:
# 	ws=None
# 	def __init__(self):
# 		print("Atm Connected")
# 		self.ws=None

# 	async def on_recieve(self,websocket,path):
# 		self.ws=websocket
# 		while True:
# 			data= await self.ws.recv()
# 			print(data)
# 	async def on_send(self,data):
# 		await self.ws.send(data)
    
# class client:
# 	ws=None
# 	def __init__(self):
# 		print("Client Connected")
# 		self.ws=None

# 	async def on_recieve(self,websocket,path):
# 		self.ws=websocket
# 		while True:
# 			data= await self.ws.recv()
# 			print(data)
# 	async def on_send(self,data):
# 		await self.ws.send(data)
    
async def handler(ws,path):
	if(path=="/atm"):
		await atm().on_recieve(ws,path)
	if(path=="/smartphone"):
		await client().on_recieve(ws,path)

start_server = websockets.serve(handler, "192.168.29.107", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()