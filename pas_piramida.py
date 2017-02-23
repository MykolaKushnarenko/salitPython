#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

def singleton(cls):
    instances = {}
    def getinstance(*args,**kvargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kvargs)
        return instances[cls]
    return getinstance


class card:
    "Карта которая имеет масть, значение и перевернутая ли она"
    names = ["", "туз"] + [str(i) for i in range(2, 11)] + ["валет", "дама", "король"]

    def __init__(self, m, val):
        self.m = m
        self.value = val
        self.opened = False

    def __repr__(self):
        return "{} {} {}".format(self.opened, self.m, card.names[self.value])

@singleton
class dump:
    def __init__(self):
        self.content = []
        for m in ["пики", "черви", "крести", "бубны"]:
            for value in range(1, 14):
                c = card(m, value)
                self.content.append(c)
        random.shuffle(self.content)

    def get_card(self):
        return self.content.pop()

@singleton
class pyramid:
    def __init__(self, d):
        self.nl = 7
        self.rows = []
        for irow in range(self.nl):
            self.rows.append([d.get_card() for icol in range(irow + 1)])
        for i in self.rows[-1]:
            i.opened = True

d = dump()
p = pyramid(d)