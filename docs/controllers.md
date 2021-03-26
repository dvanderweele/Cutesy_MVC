You can use the `cutify` tool to generate named controller files with the appropriate boilerplate. The files will already have the import statement for the function you can use to get fresh response dictionaries to fill in your controller methods. Add your own import statements for any utilities you may need, such as user-defined model classes.

Your controller classes are really just namespaces for static class methods that you are going to reference in your `routes.py` file. You can name them whatever you want, but feel free to follow resourceful naming conventions. 

Your controller methods should ideally always send back a response, even if it's just to say "no." Your controller methods will be passed one argument, the request dictionary. 

Use the `freshReponse` method to generate a fresh response dictionary to fill and return. You must pass as the first argument the request dictionary (so it can attach the appropriate client id). The second argument is optional and is a boolean indicating whether you want the original request attached to the response (defaults to false).

An example controller class: 

```python 
# UserController.py

from ..helpers.client import freshResponse 
from ..models.User import User

class UserController: 
	@staticmethod
	def index(request):
		users = User().allModels()
		res = freshResponse(request)
		res['payload'] = {
			'users': users
		}
		return res 
	@staticmethod
	def show(request):
		user = User().find(request['payload']['id'])
		res = freshResponse(request, True)
		res['payload'] = {
			'user': user
		}
		return res 
```