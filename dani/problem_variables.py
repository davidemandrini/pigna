# -*- encoding: utf-8 -*-
from classes import *

# Turni
t_m = Shift(length=8, name ="Mattina", min_p=3, max_p=3)
t_p = Shift(length=8, name ="Pomeriggio", min_p=3, max_p=3)
t_n = Shift(length=8, name ="Notte", min_p=2, max_p=2)

# Persone
n_persone = 16
persone = [Person(name = f"Operatore {i}", min_h = 0, max_h = 40) for i in range(n_persone)]

# Disponibilità
for persona in persone:
    for day in Days:
        persona.addAvailability(day, shift=t_m)
        persona.addAvailability(day, shift=t_p)
        persona.addAvailability(day, shift=t_n)
