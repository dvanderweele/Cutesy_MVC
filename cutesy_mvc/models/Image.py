from ..helpers.model import Model

class Image(Model):
	table = 'image'
	owners = ('BlogPost', 'User')
	touch = ('imageable',)
	relations = {
		'imageable': {
			'type': 'morphTo'
		}
	}
	def __str__(self):
		return f'Image: id — {self["id"]} *** URL — {self["URL"]} *** alt — {self["alt"]} *** imageable_type — {self["imageable_type"]} *** imageable_id — {self["imageable_id"]}'