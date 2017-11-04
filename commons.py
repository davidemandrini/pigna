# -*- encoding: utf-8 -*-
from enum import Enum

list_person = []
list_shift = []
list_shop = []

person_next_id = 1
shift_next_id = 1
shop_next_id = 1

def get_person_next_id():
	global person_next_id
	retval = person_next_id
	person_next_id = person_next_id + 1
	return retval

def get_shift_next_id():
	global shift_next_id
	retval = shift_next_id
	shift_next_id = shift_next_id + 1
	return retval

def get_shop_next_id():
	global shop_next_id
	retval = shop_next_id
	shop_next_id = shop_next_id + 1
	return retval

class Days(Enum):
	MONDAY = (1, "Lunedì")
	TUESDAY = (2, "Martedì")
	#WEDNESDAY = (3, "Mercoledì")
	#THURSDAY = (4, "Giovedì")
	#FRIDAY = (5, "Venerdì")
	#SATURDAY = (6, "Sabato")
	#SUNDAY = (7, "Domenica")
	
	def id(self):
		return '{0}'.format(self.value[0])

	def ita(self):
		return '{0}'.format(self.value[1])

	def get(self, idz):
		for day in Days:
			if day.value[0] == idz:
				return day

def printProblemVariables():
	print("\nNegozi:")
	for shop in list_shop:
		print(" --- {0}".format(shop))

	print("\nTurni:")
	for shift in list_shift:
		print(" --- {0} ({1} ore)".format(shift.name, shift.length))

	print("\nPersone:")
	for person in list_person:
		print(" --- {0} (min {1} ore, max {2} ore)".format(person.name, person.min_h, person.max_h))

	print("\nDisponibilità:")
	for person in list_person:
		print(" --- {0} ha {1} disponibilità".format(person, len(person.availabilities)))
		for availability in person.availabilities:
			print("  |-   {0}".format(availability))

	print("\nEsigenze negozi:")
	for shop in list_shop:
		if len(shop.presences):
			print(" --- {0}".format(shop))
			for presence in shop.presences:
				print("  |-   {0}".format(presence))
