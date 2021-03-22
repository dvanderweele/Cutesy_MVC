from ..helpers.model import Model

class Hashtag(Model):
	table = 'hashtag'
	timestamps = False
	owners = ('BlogPost', 'Video')
	relations = {
    'hashtagable': {
    	'type': 'morphTo'
    }
  }
	def __str__(self):
		return f'Hashtag: id {self["id"]} *** #{self["tag"]}'