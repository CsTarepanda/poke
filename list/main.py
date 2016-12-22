#!/usr/bin/python3
#encoding:utf-8
from data import *

for i in PokemonTypes.select().where(PokemonTypes.typedata == OriginTypes.get(name="ほのお")):
    print(i.pokemon.name)
