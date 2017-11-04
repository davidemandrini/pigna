# -*- encoding: utf-8 -*-
from enum import Enum
from commons import *

class Person:
	def __init__(self, name, min_h, max_h):
		self.id = get_person_next_id()
		self.name = name
		self.min_h = min_h
		self.max_h = max_h
		self.availabilities = []
		list_person.append(self)

	def __str__(self):
		return '{0}'.format(self.name)

	def addAvailability(self, day, shift):
		av = Availability(day, shift)
		self.availabilities.append(av)

	def getAvailability(self, day, shift):
		for av in self.availabilities:
			if av.day == day and av.shift == shift:
				return 1
		return 0

class Shift:
	def __init__(self, length, name):
		self.id =  get_shift_next_id()
		self.length = length
		self.name = name
		list_shift.append(self)

	def __str__(self):
		return '{0}'.format(self.name)

class Shop:
	def __init__(self, name):
		self.id = get_shop_next_id()
		self.name = name
		self.presences = []
		list_shop.append(self)

	def __str__(self):
		return '{0}'.format(self.name)

	def setMinPresence(self, day, shift, value):
		pr = Presence(day, shift, value)
		self.presences.append(pr)

	def getMinPresence(self, day, shift):
		for presence in self.presences:
			if presence.day == day and presence.shift == shift:
				return presence.value
		return 1

class Availability:
	def __init__(self, day, shift):
		self.day = day
		self.shift = shift

	def __str__(self):
		return '{0} {1}'.format(self.day.ita(), self.shift.name)

class Presence:
	def __init__(self, day, shift, value):
		self.day = day
		self.shift = shift
		self.value = value

	def __str__(self):
		return '{0} minimo {1} persone per il turno {2}'.format(self.day.ita(), self.value, self.shift.name)


