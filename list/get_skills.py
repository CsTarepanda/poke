#!/usr/bin/python3
#encoding: utf-8

from bs4 import BeautifulSoup
import re
from data import *
DATABASE.create_tables([SkillClassifications, Skills], True)
files = ["./skills/m{}".format(index) for index in range(10)]
# files = ["./skills/m3"]
skill_datas = []
for filename in files:
    with open(filename) as f: file_data = f.read()

    soup = BeautifulSoup(file_data, "lxml")
    skills = soup.find("table", {"summary": "技リスト"})

    def skill(tr, detail):
        s = {title[i]: x.text for i, x in enumerate(tr)}
        s.update(detail)
        # if s["Z技"] == "-":
        #     print(detail["効果"][detail["効果"].find("Z技"):])
        # else: print(s["Z技"])
        # return s["Z技"] != "-" or "Z技" in detail["効果"]
        return s

    def skill_details(tr):
        return {details_title[i]: x.text for i, x in enumerate(tr)}

    trs = skills.find_all("tr")
    title = [x.text for x in trs[0]]
    details_title = [x.text for x in trs[1]]
    # print(title)
    # print(details_title)

    for t, d in zip(trs[2::2], trs[3::2]):
        skill_data = skill(t.find_all("td"), skill_details(d.find_all("td")))
        skill_datas.append(skill_data)

    # for a in soup.find_all("a", {"href": re.compile(r"\./zukan/search/\?move=[0-9]")}):
    #     print(a)

from tqdm import tqdm
for s in tqdm(skill_datas):
    try:
        SkillClassifications.create(name=s["分類"])
    except: pass
    # Skills.create(
    #         name=s["名前"],
    #         typedata=SynonymTypes.get(SynonymTypes.name == s["タイプ"]).origin,
    #         classification=SkillClassifications.get(SkillClassifications.name == s["分類"]),
    #         power=(None if s["威力"] == "-" else int(s["威力"])),
    #         z=(None if s["Z技"] == "-" else int(s["Z技"])),
    #         pp=int(s["PP"]),
    #         accuracy=(None if s["命中"] == "-" else int(s["命中"])),
    #         guard=(s["守る"] == "守○"),
    #         direct=(s["直接"] == "直○"),
    #         info=s["効果"],
    #         target=s["対象"],
    #         )
