#!/usr/bin/python3
from bs4 import BeautifulSoup
with open("tm/2147729779268122201") as f: soup = BeautifulSoup(f.read(), "lxml")

target = "mdMTMWidget01ItemTxt01View"
for i in soup.select("p.{}".format(target)):
    print([x.previous for x in i.find_all("br")])
