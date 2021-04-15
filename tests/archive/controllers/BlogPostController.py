import time

class BlogPostController:
	@staticmethod
	def index(request = {}):
		time.sleep(2)
		print('Blog Post Controller\'s index method')