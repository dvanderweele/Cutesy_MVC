from ..helpers.model import Model

class Course(Model):
	table = 'course'
	def __str__(self):
		return f'Course: id - {self["id"]} *** title - {self["title"]} *** description - {self["description"]}'