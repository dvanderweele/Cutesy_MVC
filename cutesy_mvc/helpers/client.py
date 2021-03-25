from queue import Queue 
from threading import Thread, Lock, Event
from .server import run  
from uuid import uuid4

class Client: 
	off = Event()
	requests = Queue()
	responses = Queue()
	lock = Lock()
	server = Thread(target=run, args=(requests, responses, lock, off))
	server.start()
	clients = []
	def __init__(self):
		self.id = uuid4()
		self.__class__.clients.append(self.id)
	def __del__(self):
		self.__class__.clients.remove(self.id)
	def valid(self, identifier):
		if identifier in self.__class__.clients: 
			return True 
		else: 
			return False
	def shutdown(self):
		self.__class__.off.set()
		self.__class__.server.join()
	def freshRequest(self, route = '/'):
		return {
			'header': {
				'type': 'request',
				'route': route,
				'requester': self.id 
			},
			'payload': None 
		}
	def send(self, request):
		if not(self.__class__.off.is_set()):
			self.__class__.requests.put(request)
	def receive(self):
		with self.__class__.lock:
			if not(self.__class__.responses.empty()):
				item = self.__class__.responses.get_nowait()
				self.__class__.responses.task_done()
				return item
		return None 