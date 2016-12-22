#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import re

import os

base = "pages/"
# files = ["n1", "n3m", "n2", "n3"]
# files = ["n{}m".format(str(x)) for x in range(760, 770)]
files = os.listdir(base)
# files = os.listdir(base)[760:770]
# files = ["n750"]

from data import *
import data as database
database.DATABASE.create_tables([PokemonAbilities], True)

from tqdm import tqdm
# tqdm = lambda x: x
for f in tqdm(files):
    try:
        with open(base + f) as ff: data_file = ff.read()
    except: continue
    soup = BeautifulSoup(data_file, "lxml")

    another_form = soup.select("ul.select_list strong")
    if another_form: another_form = another_form[0].text
    kihon, detail, skill = soup.select("table")
    trs = kihon.select("tr")
    name = trs[0].text
    if name == another_form: another_form = ""
    formalname = name + ("({})".format(another_form) if another_form else "")
    target = Pokemons.get(name=formalname)

    for a in [x.text for x in detail.find_all("a", {"href": re.compile(".*tokusei.*")})]:
        pa = PokemonAbilities(pokemon=Pokemons.get(name=formalname))
        if a.startswith("*"):
            pa.hide = True
            pa.ability = Abilities.get(name=a[1:])
        else:
            pa.ability = Abilities.get(name=a)
        pa.save()
