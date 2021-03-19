from ..helpers.model import Model

class Student(Model):
	table = 'student'
	def __str__(self):
		return f'Student: id - {self["id"]}; name - {self["name"]}; dob - {self["dob"]}'