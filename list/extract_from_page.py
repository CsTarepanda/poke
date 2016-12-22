#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import re

import os
base = "pages/enco/"
# files = ["n1", "n3m", "n2", "n3"]
# files = ["n{}m".format(str(x)) for x in range(500, 810)]
files = os.listdir(base)

from data import *
import data as database
database.DATABASE.create_tables([database.Origins, database.Pokemons, database.Statuses, database.Anothers, database.PokemonTypes], True)

data = [['No.', 'ポケモン名', 'HP', '攻撃', '防御', '特攻', '特防', '素早', '合計']]
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


    # # database format
    name = trs[0].text
    if name == another_form: another_form = ""
    formalname = name + ("({})".format(another_form) if another_form else "")
    # p = Pokemon.get(Pokemons.name == formalname)
    # print(p.origin.number)

    #####################
    # ##base data
    # origin_name = name
    #
    # name_column = name
    # if another_form: name_column = (name_column, "({})".format(another_form))
    #
    # number_column = int(trs[3].find_all("td")[-1].text)
    #
    # status = list(map(lambda s: int(s if s.find("(") == -1 else s[:s.find("(")]), [tr.select("td")[1].text for tr in detail.select("tr")[1:7]]))
    # status += [sum(status)]
    #
    # data.append([number_column, name_column] + status + [origin_name])
    # #################
    # ##type list
    #
    # for tr in kihon.select("tr.center")[-2:]:
    #     tds = [td.next for td in tr.select("td")]
    #     if tds[0] == 'タイプ':
    #         for t in [SynonymTypes.get(SynonymTypes.name == x["alt"]).origin for x in tds[1].select("img")]:
    #             PokemonTypes.create(pokemon=Pokemons.get(Pokemons.name == formalname), typedata=t)
    # #################


##################################################
# print("create database...")
#
# import search
# data = [search.data_format(d) for d in data[1:]]
# search.add_mega_info(data)
# for d in tqdm(data):
#     try:
#         database.Origins.create(name=d["origin_name"], number=int(d["number"]))
#     except:
#         pass
#     if d["another"]:
#         if "another" in d["another"]:
#             p = database.Pokemons.create(
#                     origin=database.Origins.get(database.Origins.number == int(d["number"])),
#                     name="{name}({another})".format(
#                 name=d["name"],
#                 another=d["another"][1]))
#         else:
#             p = database.Pokemons.create(origin=database.Origins.get(database.Origins.number == int(d["number"])), name=d["name"])
#         database.Anothers.create(
#                 pokemon=p,
#                 another_type=d["another"][0],
#                 name=d["another"][1])
#     else:
#         p = database.Pokemons.create(origin=database.Origins.get(database.Origins.number == int(d["number"])), name=d["name"])
#         database.Anothers.create(pokemon=p)
#     database.Statuses.create(pokemon=p, **d["status"])
