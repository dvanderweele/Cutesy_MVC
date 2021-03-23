You can use the `cutify` tool to generate named controller files with the appropriate boilerplate. The files will already have the import statement for the function you can use to get fresh response objects to fill in your controller methods. Add your own import statements for any utilities you may need, such as user-defined model classes.

Your controller classes are really just namespaces for static class methods that you are going to reference in your `routes.py` file. You can name them whatever you want, but feel free to follow resourceful naming conventions. 

Your controller methods should ideally always send back a response, even if it's just to say "no." Your controller methods will be passed one argument, the request object. You may attach it in whole to the response object, or just a small part of it. At a minimum, you will probably want to attach the `uuid` that generated the request so that the main thread can route your response to the appropriate part of the user-interface.

An example controller class: 

```python 
# UserController.py

from ..helpers.client import freshResponse 
from ..models.User import User

class UserController: 
	@staticmethod
	def index(request):
		users = User().allModels()
		res = freshResponse()
		res['header']['request'] = request
		res['payload'] = {
			'users': users
		}
		return res 
	@staticmethod
	def show(request):
		user = User().find(request['payload']['id'])
		res = freshResponse()
		res['header']['request'] = request
		res['payload'] = {
			'user': user
		}
		return res 
```