from ..helpers.model import Model

class User(Model):
	table = 'user'
	relations = {
		'image': {
			'type': 'morphOne',
			'model': 'Image'
		}
	}
	def __str__(self):
		return f'User: id — {self["id"]} *** name — {self["name"]}'