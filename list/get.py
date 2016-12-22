#!/usr/bin/python3
from bs4 import BeautifulSoup
import urllib.parse as urlparse
url = "http://yakkun.com/sm/status_list.htm"

with open("poketetu_sm.data") as f: data = f.read()

soup = BeautifulSoup(data, "lxml")
for a in soup.select("div.table a"):
    print(urlparse.urljoin(url, a["href"]))
