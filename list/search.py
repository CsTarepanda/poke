#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

# url = "http://yakkun.com/xy/status_list.htm"
# response = requests.get(url)
# response.encoding = response.apparent_encoding
# data = response.text
with open("pokemon.data") as f: data = f.read()

def create_data(tag):
    more_info = tag.find("span")
    if more_info:
        more_info.extract()
        return tag.text, more_info.text
    return tag.text

soup = BeautifulSoup(data, "lxml")
table = soup.select("div.table tr")
for t in table:
    print([create_data(x) for x in t.find_all(("td", "th"))])

