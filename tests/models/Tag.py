from ..helpers.model import Model

class Tag(Model):
	table = 'tag'
	timestamps = False 
	relations = {
		'tagables': {
			'type': 'morphToMany',
			'pivot': 'Tagable'
		}
	}
	def __str__(self):
		return f'Tag {self["name"]}'