#!/usr/bin/python3
#encode: utf-8

typelist = [ "ノーマル", "ほのお", "みず", "でんき", "くさ", "こおり", "かくとう", "どく", "じめん", "ひこう", "エスパー", "むし", "いわ", "ゴースト", "ドラゴン", "あく", "はがね", "フェアリー"]
from util import *
from data import *
from tqdm import tqdm
synonym = [
        # [ "ノ", "炎", "水", "電", "草", "氷", "格", "毒", "地", "飛", "超", "虫", "岩", "霊", "竜", "悪", "鋼", "妖"],
        # [katakana(x) for x in typelist],
        # [hiragana(x) for x in typelist],
        # [hiragana(x)[0] for x in typelist],
        # [katakana(x)[0] for x in typelist],
        ]
#
DATABASE.create_tables([OriginTypes, SynonymTypes], True)

for t1 in tqdm(zip(typelist, *synonym)):
    try:
        t = OriginTypes.create(name=t1[0])
    except:
        t = OriginTypes.get(OriginTypes.name == t1[0])
    for t2 in t1[1:]:
        SynonymTypes.create(name=t2, origin=t)

