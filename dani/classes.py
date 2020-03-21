# -*- encoding: utf-8 -*-
from enum import Enum
from commons import *


class Person:
    def __init__(self, name, min_h, max_h):
        self.id = get_person_next_id()
        self.name = name
        self.min_h = min_h
        self.max_h = max_h
        self.availabilities = []
        list_person.append(self)

    def __str__(self):
        return f"ID: {self.id} - Name: {self.name} - Min: {self.min_h}h - Max: {self.max_h}h"

    def addAvailability(self, day, shift):
        av = Availability(day, shift)
        self.availabilities.append(av)

    def getAvailability(self, day, shift):
        for av in self.availabilities:
            if av.day == day and av.shift == shift:
                return 1
        return 0


class Shift:
    def __init__(self, length, name, min_p, max_p):
        self.id = get_shift_next_id()
        self.length = length
        self.name = name
        self.min_p = min_p
        self.max_p = max_p
        list_shift.append(self)

    def __str__(self):
        return f"Turno: {self.id} - Durata: {self.length}h - Nome: {self.name} - Min {self.min_p} persone - Max {self.max_p} persone"


class Availability:
    def __init__(self, day, shift):
        self.day = day
        self.shift = shift

    def __str__(self):
        return f"{self.day} - {self.shift}"
