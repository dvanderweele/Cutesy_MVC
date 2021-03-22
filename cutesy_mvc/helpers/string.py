from ..routes import definitions

def process(request = {'route': None}):
	res = {}
	for r in definitions.items():
		if r[0] == request['route']:
			res = r[1](request)
			break 
	
	