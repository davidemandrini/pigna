# -*- encoding: utf-8 -*-
from enum import Enum
from commons import *
import math


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

    def get_next(self, day_id, step=1, num_shifts=3):
        next_shift = ((self.id - 1 + step) % num_shifts) + 1
        delta_day = 0
        rr = range(self.id + 1, self.id + 1 + step)
        #print(list(rr))
        for i in rr:
            if i % num_shifts == 1:
                delta_day += 1
        next_day = ((day_id - 1 + delta_day) % 7 ) + 1
        return (next_shift, next_day)

class Availability:
    def __init__(self, day, shift):
        self.day = day
        self.shift = shift

    def __str__(self):
        return f"{self.day} - {self.shift}"
