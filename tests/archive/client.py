from cutesy_mvc.helpers.router import process 
from cutesy_mvc.helpers.client import Client 
import time 


c = Client()
c.send({
	'header': {
		'type': 'request',
		'route': '/blog/index'
	},
	'payload': None
})
for i in range(10):
	print(i)
c.shutdown()