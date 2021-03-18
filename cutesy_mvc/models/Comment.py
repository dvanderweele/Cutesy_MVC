from ..helpers.model import Model

class Comment(Model):
	table = 'comment'
	relations = {
	  'blogPost': {
	    'type': 'belongsTo',
	    'model': 'BlogPost'
	  }
	}