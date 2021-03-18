from ..helpers.model import Model

class BlogPost(Model):
  softDeletes = True
  table = 'blog_post'
  relations = {
    'comments': {
      'type': 'hasMany',
      'model': 'Comment'
    }
  }
  def __str__(self):
    return f'Title: {self["title"]} *** Body: {self["body"]}'