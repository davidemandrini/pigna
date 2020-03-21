# -*- encoding: utf-8 -*-
from pulp import *
from problem_variables import *
import collections

day_dict = {d.id(): d for d in Days}
shift_dict = {s.id: s for s in list_shift}
person_dict = {p.id: p for p in list_person}

variables = (day_dict.keys(), shift_dict.keys(), person_dict.keys())

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Turni_Dani", LpMinimize)
var = LpVariable.dicts("var", variables, 0, 1, LpInteger)

# The objective function is added to 'prob' first
# The arbitrary objective function is added: there is no good or bad solution,
# a solution that respect all contraints is enough
prob += 0

# The constraints are added to 'prob'
# 1. Ogni lavoratore puo lavorare un minimo di ore
for person_id in person_dict:
    prob += lpSum([var[day_id][shift_id][person_id] * shift_dict[shift_id].length
                   for day_id in day_dict for shift_id in shift_dict]) \
            >= person_dict[person_id].min_h, ""

# 2. Ogni lavoratore puo lavorare un massimo di ore
for person_id in person_dict:
    prob += lpSum([var[day_id][shift_id][person_id] * shift_dict[shift_id].length
                   for day_id in day_dict for shift_id in shift_dict]) \
            <= person_dict[person_id].max_h, ""

# 3. Ogni lavoratore puo lavorare in al massimo un turno alla volta
for person_id in person_dict:
    for day_id in day_dict:
        for shift_id in shift_dict:
            prob += var[day_id][shift_id][person_id] <= 1

# 4. Ogni turno e' coperto dal numero minimo di persone
for shift_id in shift_dict:
    for day_id in day_dict:
        prob += lpSum([var[day_id][shift_id][person_id] for person_id in person_dict]) \
                >= shift_dict[shift_id].min_p, ""

# 5. Ogni turno e' coperto dal numero massimo di persone
for shift_id in shift_dict:
    for day_id in day_dict:
        prob += lpSum([var[day_id][shift_id][person_id] for person_id in person_dict]) \
                <= shift_dict[shift_id].max_p, ""

# 6. Ogni lavoratore deve lavorare solo quando ha dato la sua disponibilita'
for day_id in day_dict:
    for shift_id in shift_dict:
        for person_id in person_dict:
            prob += var[day_id][shift_id][person_id] <= person_dict[person_id].getAvailability(day_dict[day_id], shift_dict[shift_id])

# 7. Ogni lavoratore lavora al massimo un turno per giornata
for person_id in person_dict:
    for day_id in day_dict:
        prob += lpSum([var[day_id][shift_id][person_id] for shift_id in shift_dict]) \
                <= 1, ""

# Print problem variables
printProblemVariables()

max_sol = 1
cur_sol = 0

while cur_sol < max_sol:

    prob.solve()

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    # Get the status of the solution
    success = LpStatus[prob.status] == "Optimal"

    # The solution is printed if it was deemed "optimal" i.e met the constraints
    if success:

        # prepare structure for results
        res_turni = collections.OrderedDict()
        for day_id in day_dict:
            res_turni[day_id] = collections.OrderedDict()
            for shift_id in shift_dict:
                res_turni[day_id][shift_id] = []

        res_persone = collections.OrderedDict()
        for person_id in person_dict:
            res_persone[person_id] = collections.OrderedDict()
            for day_id in day_dict:
                res_persone[person_id][day_id] = []

        # Process results
        for v in prob.variables():
            if v.varValue == 1:
                day_id, shift_id, person_id = map(lambda x: int(x), v.name.split("_")[1:])
                res_turni[day_id][shift_id].append(person_id)
                res_persone[person_id][day_id].append(shift_id)

        # Print results per day/shift
        print("\nTurni:")
        for day_id in res_turni:
            print(f"-- {Days.LUNEDI.get(day_id).ita()}")
            for shift_id in res_turni[day_id]:
                print(f"\tTurno {shift_dict[shift_id].id}: {', '.join([person_dict[s].name for s in res_turni[day_id][shift_id]])}")

        # Print results per person
        print("\nPer persona:")
        for person_id in res_persone:
            tot = 0
            print(f"-- {person_dict[person_id].name}")
            for day_id in res_persone[person_id]:
                curr_turni = [str(shift_dict[s].id) for s in res_persone[person_id][day_id]]
                tot += len(curr_turni)
                if len(curr_turni) > 0:
                    print(f"\t{day_dict[day_id].ita()} - turni: {', '.join(curr_turni)}")
            print(f"\tTotale: {tot} turni")

        # The constraint is added that the same solution cannot be returned again
        prob += lpSum([var[day_id][shift_id][person_id]
                       for day_id in day_dict for shift_id in shift_dict for person_id in person_dict
                       if value(var[day_id][shift_id][person_id]) == 1]) <= 55 # (( 3 + 3 + 2 ) * 7 ) - 1

        cur_sol += 1
    # If a new optimal solution cannot be found, we end the program
    else:
        break