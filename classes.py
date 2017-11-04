# -*- encoding: utf-8 -*-
from enum import Enum

staff = []
shops = []
shifts = []

class Day(Enum):
	MONDAY = (1, "Lunedì")
	TUESDAY = (2, "Martedì")
	#WEDNESDAY = (3, "Mercoledì")
	#THURSDAY = (4, "Giovedì")
	#FRIDAY = (5, "Venerdì")
	#SATURDAY = (6, "Sabato")
	#SUNDAY = (7, "Domenica")
	def __str__(self):
		return '{0}'.format(self.value[1])

class Person:
	def __init__(self, name, lastname, min_h, max_h):
		self.name = name
		self.lastname = lastname
		self.min_h = min_h
		self.max_h = max_h
		self.availabilities = []
		staff.append(self)
	def __str__(self):
		return '{0} {1}'.format(self.name, self.lastname)
	def addAvailability(self, day, shift):
		av = Availability(day, shift)
		self.availabilities.append(av)
	def getAvailability(self, day, shift):
		for av in self.availabilities:
			if av.day == day and av.shift == shift:
				return 1
		return 0

class Shift:
	def __init__(self, id, hours, name):
		self.id = id
		self.hours = hours
		self.name = name
		shifts.append(self)
	def __str__(self):
		return '{0} ({1} ore)'.format(self.name, self.hours)

class Shop:
	def __init__(self, name):
		self.name = name
		self.presences = []
		shops.append(self)
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
		return '{0} {1}'.format(self.day.value[1], self.shift.name)

class Presence:
	def __init__(self, day, shift, value):
		self.day = day
		self.shift = shift
		self.value = value
	def __str__(self):
		return '{0} minimo {1} persone per il turno {2}'.format(self.day.value[1], self.value, self.shift.name)
