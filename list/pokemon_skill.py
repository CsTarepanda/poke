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
# files = ["n26a"]

from data import *
import data as database
database.DATABASE.create_tables([PokemonSkills], True)

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

    for s in skill.select("tr.c1"):
        line = [td.text for td in s.find_all("td")]
        if not line[1]: continue
        line[0] = re.sub("\..*", "", line[0])
        line[1] = re.sub("\(.*\)", "", line[1])
        PokemonSkills.create(pokemon=target, skill=Skills.get(name=line[1]), classification=line[0])
