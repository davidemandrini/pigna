# -*- encoding: utf-8 -*-
from pulp import *
from commons import *
from problem_variables import *

shop_dict = {s.id : s for s in list_shop}
day_dict = {d.id() : d for d in Days}
shift_dict = {s.id : s for s in list_shift}
person_dict = {p.id : p for p in list_person}

variables = (shop_dict.keys(), day_dict.keys(), shift_dict.keys(), person_dict.keys())

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Turni Pigna", LpMinimize)
var = LpVariable.dicts("var", variables, 0, 1, LpInteger)

# The objective function is added to 'prob' first
# The arbitrary objective function is added: there is no good or bad solution, a solution that respect all contraints is enough
prob += 0

# The constraints are added to 'prob'
# 1. Ogni lavoratore puo lavorare un minimo di ore
for person_id in person_dict:
	prob += lpSum([var[shop_id][day_id][shift_id][person_id]*shift_dict[shift_id].length for shop_id in shop_dict for day_id in day_dict for shift_id in shift_dict]) >= person_dict[person_id].min_h, ""

# 2. Ogni lavoratore puo lavorare un massimo di ore
for person_id in person_dict:
	prob += lpSum([var[shop_id][day_id][shift_id][person_id]*shift_dict[shift_id].length for shop_id in shop_dict for day_id in day_dict for shift_id in shift_dict]) <= person_dict[person_id].max_h, ""

# 3. Ogni lavoratore puo lavorare in al massimo un negozio in un determinato giorno/fascia
for person_id in person_dict:
	for day_id in day_dict:
		for shift_id in shift_dict:
			prob += lpSum([var[shop_id][day_id][shift_id][person_id] for shop_id in shop_dict]) <= 1, ""

# 3. Ogni negozio deve avere sempre una persona al giorno e per fascia. Alcuni negozi hanno delle esigenze particolari e richiedono piu' di una persona
for shop_id in shop_dict:
	for day_id in day_dict:
		for shift_id in shift_dict:
			prob += lpSum([var[shop_id][day_id][shift_id][person_id] for person_id in person_dict]) == shop_dict[shop_id].getMinPresence(day_dict[day_id], shift_dict[shift_id]), ""

# 4. Ogni lavoratore deve lavorare solo quando ha dato la sua disponibilita'
for shop_id in shop_dict:
	for day_id in day_dict:
		for shift_id in shift_dict:
			for person_id in person_dict:
				prob += var[shop_id][day_id][shift_id][person_id] <= person_dict[person_id].getAvailability(day_dict[day_id], shift_dict[shift_id])

# The problem is solved using PuLP's choice of Solver
prob.solve()

# Get the status of the solution
success = LpStatus[prob.status] == "Optimal"

# Print problem variables
printProblemVariables()

# Print results
print("\nTurni:")
if success:
	for v in prob.variables():
		if v.varValue == 1:
			shop_id, day_id, shift_id, person_id = map(lambda x : int(x), v.name.split("_")[1:])
			shop = shop_dict.get(shop_id)
			day = Days.MONDAY.get(day_id) # bad workaround to get the day by id
			shift = shift_dict.get(shift_id)
			person = person_dict.get(person_id)
			print("{0}\t{1}\t{2}\t{3}".format(shop, day.ita(), shift, person))
else:
	print("Pigna qui non si fanno miracoli...")
