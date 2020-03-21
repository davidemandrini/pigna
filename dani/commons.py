# -*- encoding: utf-8 -*-
from enum import Enum

list_person = []
list_shift = []

person_next_id = 1
shift_next_id = 1


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


class Days(Enum):
    LUNEDI = (1, "Lunedì")
    MARTEDI = (2, "Martedì")
    MERCOLEDI = (3, "Mercoledì")
    GIOVEDI = (4, "Giovedì")
    VENERDI = (5, "Venerdì")
    SABATO = (6, "Sabato")
    DOMENICA = (7, "Domenica")

    def id(self):
        return self.value[0]

    def ita(self):
        return self.value[1]

    def get(self, idz):
        for day in Days:
            if day.value[0] == idz:
                return day


def printProblemVariables():
    print("\nTurni:")
    for shift in list_shift:
        print(" --- {0}".format(shift))

    print("\nPersone:")
    for person in list_person:
        print(" --- {0} ".format(person))

    print("\nDisponibilità:")
    for person in list_person:
        print(" --- {0} ha {1} disponibilità".format(person.name, len(person.availabilities)))
        for availability in person.availabilities:
            print("  |-   Turno {0} - {1}".format(availability.shift.id, availability.day.ita()))
