from ..helpers.model import Model

class Comment(Model):
	table = 'comment'
	relations = {
	  'blogPost': {
	    'type': 'belongsTo',
	    'model': 'BlogPost'
	  }
	}
	def __str__(self):
		return f'Comment: id {self["id"]} *** body {self["body"]}'