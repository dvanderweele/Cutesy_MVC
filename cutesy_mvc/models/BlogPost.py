from ..helpers.model import Model

class BlogPost(Model):
  softDeletes = True
  table = 'blog_post'
  relations = {
    'comments': {
      'type': 'hasMany',
      'model': 'Comment'
    },
    'image': {
    	'type': 'morphOne',
    	'model': 'Image'
    }
  }
  def __str__(self):
    return f'id: {self["id"]} *** Title: {self["title"]} *** Body: {self["body"]} *** Deleted_at: {str(self["deleted_at"])}'