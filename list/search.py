#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import re

# url = "http://yakkun.com/xy/status_list.htm"
# url = "http://blog.game-de.com/pm-sm/sm-allstats/"
# url = "http://yakkun.com/sm/status_list.htm"
# response = requests.get(url)
# response.encoding = response.apparent_encoding
# data = response.text
# with open("poketetu_sm.data", "w") as f: f.write(data)

def create_data_poketetu(tag):
    more_info = tag.find("span")
    if more_info:
        more_info.extract()
        return tag.text, more_info.text
    return tag.text

def create_data_DEcom(tag, pokename):
    get = [0, 1, 4, 5, 6, 7, 8, 9, 10]
    data = [tag[x].text for x in get]
    if "-" in data[0]:
        data[0] = data[0][:data[0].find("-")]
    data[1] = re.sub(r"( +|UB#)", "", data[1])
    if data[1].endswith(":A"):
        data[1] = "{}(アローラのすがた)".format(data[1][:-2])

    if data[1] in pokename:
        data[1] = pokename[data[1]]
    if re.match(".+\(.*\)", data[1]):
        data[1] = (data[1][:data[1].index("(")], data[1][data[1].index("("):data[1].index(")") + 1])
    return data

def poketetu():
    with open("poketetu_sm.data") as f: data = f.read()
    soup = BeautifulSoup(data, "lxml")

    table = soup.select("div.table tr")
    return [[create_data_poketetu(x) for x in t.find_all(("td", "th"))] for t in table]

def DEcom():
    with open("pokemon_sm.data") as f: data = f.read()
    soup = BeautifulSoup(data, "lxml")

    table = soup.select("table tr")
    pokename = soup.select("div .mini ul")[0]
    pokename = {k: v for k, v in [li.text.split(":") for li in pokename.find_all("li")]}
    return [create_data_DEcom(t.find_all(("td", "th")), pokename) for t in table]

data = poketetu()
#
# from data import *
# DATABASE.create_tables([Pokemon, Status, Another, Evolution, MegaEvolution], True)

def data_format(data):
    result = {
            "number": int(data[0]),
            "name": None, "another": None,
            "status": {
                "hp": int(data[2]),
                "attack": int(data[3]),  
                "block": int(data[4]),
                "contact": int(data[5]),
                "defence": int(data[6]),
                "speed": int(data[7]),
                "summation": int(data[8]),
                },
            "origin_name": data[9], # if get data from pages
            }
    if type(data[1]) == str:
        result["name"] = data[1]
    else:
        result["name"] = data[1][0]
        result["another"] = ["another", data[1][1][1:-1]]
    return result

def add_mega_info(data):
    numbers = {}
    for index, d in enumerate(data):
        if d["number"] in numbers and not d["another"]:
            if d["name"].startswith("メガ"):
                d["another"] = ["mega", d["name"]]
                d["origin_name"] = numbers[d["number"]][0]
            elif numbers[d["number"]][0].startswith("メガ"):
                data[numbers[d["number"]][1]]["another"] = ["mega", numbers[d["number"]][0]]
                data[numbers[d["number"]][1]]["origin_name"] = d["name"]

            elif d["name"].startswith("ゲンシ"):
                d["another"] = ["genshi", d["name"]]
                d["origin_name"] = numbers[d["number"]][0]
            elif numbers[d["number"]][0].startswith("ゲンシ"):
                data[numbers[d["number"]][1]]["another"] = ["genshi", numbers[d["number"]][0]]
                data[numbers[d["number"]][1]]["origin_name"] = d["name"]
        else:
            numbers[d["number"]] = (d["name"], index)


# print(data)
##################################################
#format::
#[['No.', 'ポケモン名', 'HP', '攻撃', '防御', '特攻', '特防', '素早', '合計'],
#   [...], ,[..., ('name', '(another_form)'), ...],
#]
##################################################
# import data as database
# database.DATABASE.create_tables([database.Origin, database.Pokemon, database.Status, database.Another], True)
#
# data = [data_format(d) for d in data[1:]]
# add_mega_info(data)
# number = None
# for d in data:
#     if d["number"] != number:
#         database.Origin.create(name=d["name"], number=int(d["number"]))
#         number = d["number"]
#     if d["another"]:
#         if "another" in d["another"]:
#             p = database.Pokemon.create(
#                     origin=database.Origin.get(database.Origin.number == int(d["number"])),
#                     name="{name}({another})".format(
#                 name=d["name"],
#                 another=d["another"][1]))
#         else:
#             p = database.Pokemon.create(origin=database.Origin.get(database.Origin.number == int(d["number"])), name=d["name"])
#         database.Another.create(
#                 pokemon=p,
#                 another_type=d["another"][0],
#                 name=d["another"][1])
#     else:
#         p = database.Pokemon.create(origin=database.Origin.get(database.Origin.number == int(d["number"])), name=d["name"])
#         database.Another.create(
#                 pokemon=p,
#                 another_type="none",
#                 name="none")
#     database.Status.create(pokemon=p, **d["status"])
