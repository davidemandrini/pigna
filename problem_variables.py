# -*- encoding: utf-8 -*-
from classes import *

# Turni
turno1 = Shift(length = 2, name = "10:00 - 11:59")
turno2 = Shift(length = 3, name = "12:00 - 14:59")

# Persone
persona1 = Person(name = "Davide", min_h = 0, max_h = 3)
persona2 = Person(name = "Fabio", min_h = 0, max_h = 20)
persona3 = Person(name = "Cristiano", min_h = 0, max_h = 20)

# Disponibilità
persona1.addAvailability(day = Days.MONDAY, shift = turno1)
persona1.addAvailability(day = Days.TUESDAY, shift = turno1)

persona2.addAvailability(day = Days.MONDAY, shift = turno1)
persona2.addAvailability(day = Days.MONDAY, shift = turno2)
persona2.addAvailability(day = Days.TUESDAY, shift = turno1)
persona2.addAvailability(day = Days.TUESDAY, shift = turno2)

persona3.addAvailability(day = Days.MONDAY, shift = turno1)
persona3.addAvailability(day = Days.MONDAY, shift = turno2)
persona3.addAvailability(day = Days.TUESDAY, shift = turno1)
persona3.addAvailability(day = Days.TUESDAY, shift = turno2)

# Negozi
negozio1 = Shop("Negozio 1")
negozio2 = Shop("Negozio 2")

# Persone minime per negozio
negozio1.setMinPresence(day = Days.MONDAY, shift = turno1, value = 2)