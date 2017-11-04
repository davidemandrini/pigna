# -*- encoding: utf-8 -*-

from pulp import *
from classes import *
from parameters import *

giorni = {d.name : d for d in Day}
persone = {p.name : p for p in staff}
fasce = {s.name : s for s in shifts}
negozi = {n.name : n for n in shops}

variables = [ (n, g, f, p) for n in negozi.keys()for g in giorni.keys() for f in fasce.keys() for p in persone.keys() ]

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Turni Pigna", LpMinimize)

var = LpVariable.dicts("var", variables, 0, 1, LpInteger)

# The objective function is added to 'prob' first
# The arbitrary objective function is added: there is no good or bad solution, a solution that respect all contraints is enough
prob += 0

# The constraints are added to 'prob'

# Ogni lavoratore puo lavorare un minimo di ore
for p in persone:
	prob += lpSum([var[n, g, f, p]*fasce[f].hours for n in negozi for g in giorni for f in fasce]) >= persone[p].min_h, ""

# Ogni lavoratore puo lavorare un massimo di ore
for p in persone:
	prob += lpSum([var[n, g, f, p]*fasce[f].hours for n in negozi for g in giorni for f in fasce]) <= persone[p].max_h, ""

# Ogni lavoratore puo lavorare in al massimo un negozio in un determinato giorno/fascia
for p in persone:
	for g in giorni:
		for f in fasce:
			prob += lpSum([var[n, g, f, p] for n in negozi]) <= 1, ""

# Ogni negozio deve avere sempre una persona al giorno e per fascia
# Alcuni negozi hanno delle esigenze particolari e richiedono piu' di una persona
for n in negozi:
	for g in giorni:
		for f in fasce:
			prob += lpSum([var[n, g, f, p] for p in persone]) == negozi[n].getMinPresence(giorni[g], fasce[f]), ""

# Ogni lavoratore deve lavorare solo quando ha dato la sua disponibilita'
for n in negozi:
	for g in giorni:
		for f in fasce:
			for p in persone:
				prob += var[n, g, f, p] <= persone[p].getAvailability(giorni[g], fasce[f])

# The problem is solved using PuLP's choice of Solver
prob.solve()
print(prob)

# The status of the solution is printed to the screen
success = LpStatus[prob.status] == "Optimal"

# Each of the variables is printed with it's resolved optimum value
if success:
	for v in prob.variables():
		if v.varValue == 1:
			print(v)
else:
	print("Pigna qui non si fanno miracoli...")
