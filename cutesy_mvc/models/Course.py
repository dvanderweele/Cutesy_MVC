from ..helpers.model import Model

class Course(Model):
	table = 'course'
	relations = {
		'students': {
			'type': 'belongsToMany',
			'model': 'Student',
			'pivot': 'Schedule'
		}
	}
	def __str__(self):
		return f'Course: id - {self["id"]} *** title - {self["title"]} *** description - {self["description"]}'