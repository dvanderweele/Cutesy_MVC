from .controllers.BlogPostController import BlogPostController

definitions = (
	('/blog/index', BlogPostController.index),
)