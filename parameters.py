# -*- encoding: utf-8 -*-

from classes import *

# Turni
turno1 = Shift(id = 1, hours = 2, name = "10:00 - 11:59")
turno2 = Shift(id = 2, hours = 3, name = "12:00 - 14:59")

# Persone
persona1 = Person(name = "Davide", lastname = "Mandrini", min_h = 0, max_h = 3)
persona2 = Person(name = "Fabio", lastname =  "Pignataro", min_h = 0, max_h = 20)
persona3 = Person(name = "Cristiano", lastname =  "Ronaldo", min_h = 0, max_h = 20)

# Disponibilità
persona1.addAvailability(day = Day.MONDAY, shift = turno1)
persona1.addAvailability(day = Day.TUESDAY, shift = turno1)

persona2.addAvailability(day = Day.MONDAY, shift = turno1)
persona2.addAvailability(day = Day.TUESDAY, shift = turno1)
persona2.addAvailability(day = Day.MONDAY, shift = turno2)
persona2.addAvailability(day = Day.TUESDAY, shift = turno2)

persona3.addAvailability(day = Day.MONDAY, shift = turno1)
persona3.addAvailability(day = Day.MONDAY, shift = turno2)
persona3.addAvailability(day = Day.TUESDAY, shift = turno1)
persona3.addAvailability(day = Day.TUESDAY, shift = turno2)

# Negozi""
negozio1 = Shop("Negozio Lago di Caiazzo")
negozio2 = Shop("Negozio Lago di Gargiulo")

# Persone minime per negozio
negozio1.setMinPresence(day = Day.MONDAY, shift = turno1, value = 2)


# ################################################################
# Stampa riassunto della situazione
# ################################################################
print("Negozi:")
for s in shops:
	print(" - {0}".format(s))

print("Turni:")
for s in shifts:
	print(" - {0}".format(s))

print("Persone:")
for s in staff:
	print(" - {0} (min {1} ore, max {2} ore)".format(s, s.min_h, s.max_h))

print("Disponibilità:")
for p in staff:
	print(" - {0}, {1} disponibilità".format(p, len(p.availabilities)))
	for av in p.availabilities:
		print("     {0}".format(av))

print("Esigenze negozi")
for s in shops:
	if len(s.presences):
		print(" - {0}".format(s))
		for pr in s.presences:
			print("     {0}".format(pr))


