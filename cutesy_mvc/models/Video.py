from ..helpers.model import Model

class Video(Model):
	table = 'video'
	timestamps = False
	relations = {
		'hashtags': {
			'type': 'morphMany',
			'model': 'Hashtag'
		}
	}
	def __str__(self):
		return f'Video: id {self["id"]} *** title {self["title"]}'