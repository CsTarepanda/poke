#!/usr/bin/python3
#encoding: utf-8

from bs4 import BeautifulSoup
import re
from data import *
DATABASE.create_tables([Abilities], True)

with open("./tm/ability_list.htm") as f: soup = BeautifulSoup(f.read(), "lxml")

abilities = [(lambda y: (y, y.next.text))(x.next.next) for x in soup.select("td.c1")]
from tqdm import tqdm
for a in tqdm(abilities):
    Abilities.create(name=a[0], info=a[1])
