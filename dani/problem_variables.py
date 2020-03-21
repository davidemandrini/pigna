# -*- encoding: utf-8 -*-
from classes import *

# Turni
turno1 = Shift(length=8, name ="07:00 - 15:00", min_p=3, max_p=3)
turno2 = Shift(length=8, name ="15:00 - 23:00", min_p=3, max_p=3)
turno3 = Shift(length=8, name ="23:00 - 07:00", min_p=2, max_p=2)

# Persone
n_persone = 16
persone = [Person(name = f"Operatore {i}", min_h = 0, max_h = 40) for i in range(n_persone)]

# Disponibilità
for persona in persone:
    for day in Days:
        persona.addAvailability(day, shift=turno1)
        persona.addAvailability(day, shift=turno2)
        persona.addAvailability(day, shift=turno3)
