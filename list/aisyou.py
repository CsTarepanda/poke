#!/usr/bin/python3
from bs4 import BeautifulSoup
from data import *
DATABASE.create_tables([TypeChemistries], True)
with open("aisyou.html") as f: data = f.read()

soup = BeautifulSoup(data, "lxml")
table = soup("table", {"summary": "タイプ相性表サンムーン"})[0]
atk = [x.text for x in table.select("tr")[1].select("td")]
dfc = [[x.text for x in tr.select("td")] for tr in table.select("tr")[2:len(atk) + 2]]

r = {"\xa0": "  ", "▲": "△ ", "●": "◯ ", "×": "x "}
n = {"\xa0": 1.0, "▲": 0.5, "●": 2.0, "×": 0.0}

dfc = [[line[0]] + [n[x] for x in line[1:]] for line in dfc]

def check(arrays, array2):
    for array1 in arrays:
        if array1[0] == array2[0] and array1[1] == array2[1]:
            return False
    else:
        return True

from tqdm import tqdm
pair = []
for d in tqdm(dfc):
    for chem in [[x, atk[i], d[0]] for i, x in enumerate(d[1:])]:
        if check(pair, chem[1:3]):
            TypeChemistries.create(
                    effective=chem[0],
                    atk=SynonymTypes.get(SynonymTypes.name == chem[2]).origin,
                    dfc=SynonymTypes.get(SynonymTypes.name == chem[1]).origin)
            pair.append(chem[1:3])
# print("  ", " ".join(atk))
# for line in dfc:
#     print(" ".join(line))
