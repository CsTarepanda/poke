#!/usr/bin/python3
#encoding:utf-8
from data import *

bug = OriginTypes.get(name='むし')
water = OriginTypes.get(name='みず')

for t in OriginTypes.select():
    print(t.atks.where(TypeChemistries.effective < 1).count(), end=": ")
    print([x.dfc.name for x in t.atks.where(TypeChemistries.effective < 1)])
