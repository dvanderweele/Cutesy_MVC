from ..routes import definitions 

def process(request = {'header':{'type':'request','route':'/'},'payload': None}):
	for r in definitions:
		if r[0] == request['header']['route']:
			return r[1](request)
	return {
		'header': {
			'type': 'response'
		},
		'payload': None
	}
		