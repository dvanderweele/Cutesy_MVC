from ..helpers.model import Model

class Tagable(Model):
	table = 'tagable'
	timestamps = False 
	morphs = ('BlogPost', 'Video')
	relations = {
		'tag': {
			'type': 'poly',
			'model': 'Tag'
		}
	}