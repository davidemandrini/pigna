# -*- encoding: utf-8 -*-
from pulp import *
from problem_variables import *
import collections

day_dict    = collections.OrderedDict({d.id(): d for d in Days})
shift_dict  = collections.OrderedDict({s.id  : s for s in list_shift})
person_dict = collections.OrderedDict({p.id  : p for p in list_person})

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

# 8. Ogni lavoratore ha un break di almeno 2 shifts
for person_id in person_dict:
    for day_id in day_dict:
        for shift_id in shift_dict:
            next1_shift_id, next1_day_id = shift_dict[shift_id].get_next(day_id, step=1, num_shifts=3)
            next2_shift_id, next2_day_id = shift_dict[shift_id].get_next(day_id, step=2, num_shifts=3)
            zipped = zip([shift_id, next1_shift_id, next2_shift_id], [day_id, next1_day_id, next2_day_id])
            #print("(shift, day)")
            #print(list(zipped))
            try:
                #print([var[d][s][person_id] for (s, d) in zipped])
                prob += lpSum([var[d][s][person_id] for (s, d) in zipped])\
                        <= 1, ""
            except KeyError:
                print("pers", person_id, "day", day_id, "shift", shift_id)
                print("next shift", next1_shift_id, "next_day", next1_day_id)
                print("next shift", next2_shift_id, "next_day", next2_day_id)
                print("(shift, day)")
                print(list(zipped))
                break

# Print problem variables
printProblemVariables()

def check_min_break(res_persone, n_shifts=3):
    tot_invalid = 0
    for person_id in res_persone:
        for day_id in res_persone[person_id]:
            cur_day_shift = res_persone[person_id][day_id]
            prev_day_shift = res_persone[person_id].get(day_id-1, None)
            if prev_day_shift and len(prev_day_shift) > 0 and len(cur_day_shift) > 0:
                # we have a previous day shift, so we need to check the distance
                if cur_day_shift[0]+3 - prev_day_shift[0] < n_shifts:
                    print(Days.LUNEDI.get(day_id - 1), prev_day_shift, Days.LUNEDI.get(day_id), cur_day_shift)
                    print("Invalid: ", person_dict[person_id].name, str(res_persone[person_id]))
                    tot_invalid += 1
    return True if tot_invalid <= 0 else False

max_valid_sol = 2
count_valid_sol = 0

while True:

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

        # can't work twice in a moving windows of 3 shifts
        valid_sol = check_min_break(res_persone, n_shifts=3)

        if not valid_sol:
            print("Invalid solution found, check with Davide")
            break

        else:
            print("Valid solution found!")

            # Print results per day/shift
            print("\nTurni:")
            for day_id in res_turni:
                print(f"-- {Days.LUNEDI.get(day_id).ita()}")
                for shift_id in res_turni[day_id]:
                    print(
                        f"\tTurno {shift_dict[shift_id].name}: {', '.join([person_dict[s].name for s in res_turni[day_id][shift_id]])}")

            # Print results per person
            print("\nPer persona:")
            for person_id in res_persone:
                tot = 0
                print(f"-- {person_dict[person_id].name}")
                for day_id in res_persone[person_id]:
                    curr_turni = [str(shift_dict[s].name) for s in res_persone[person_id][day_id]]
                    tot += len(curr_turni)
                    if len(curr_turni) > 0:
                        print(f"\t{day_dict[day_id].ita()} - turni: {', '.join(curr_turni)}")
                print(f"\tTotale: {tot} turni")

            # Add constraint in case we want to compute a further solution
            prob += lpSum([var[day_id][shift_id][person_id]
                           for day_id in day_dict for shift_id in shift_dict for person_id in person_dict
                           if value(var[day_id][shift_id][person_id]) == 1]) <= 55  #  <= (( 3 + 3 + 2 ) * 7 ) - 1

            # a valid solution has been found, we increment the count of valid solutions
            count_valid_sol += 1
            if count_valid_sol >= max_valid_sol:
                print("Found the max number of valid solutions")
                break

    # If a new optimal solution cannot be found, we end the program
    else:
        print("Cannot find an optimal solution anymore")
        break


