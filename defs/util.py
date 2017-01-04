#!/usr/bin/python3
#encoding: utf-8
import re

def make_function_hiragana():
    re_katakana = re.compile('[ァ-ヴ]')
    def hiragana(text):
        """ひらがな変換"""
        return re_katakana.sub(lambda x: chr(ord(x.group(0)) - 0x60), text)
    return hiragana
hiragana = make_function_hiragana()


def make_function_katakana():
    re_hiragana = re.compile('[ぁ-ゔ]')
    def katakana(text):
        """カタカナ変換"""
        return re_hiragana.sub(lambda x: chr(ord(x.group(0)) + 0x60), text)
    return katakana
katakana = make_function_katakana()


def calc_status(status, effort={}, nature="まじめ", level=50):
    if not nature: nature = "まじめ"
    ef = {"h":0, "a":0, "b":0, "c":0, "d":0, "s":0}
    efs = {"a":"attack", "b":"block", "c":"contact", "d":"defence", "s":"speed"}
    ef.update(effort)
    h = ((status.hp*2 + 31 + ef["h"]/4) * level / 100) + 10 + level
    return {name: int(h if name == "h" else int(((getattr(status, efs[name]) * 2 + 31 + value / 4) * level / 100) + 5) * NATURE[nature][NATURE_INDEX[name]]) for name, value in ef.items()}

MAX = 252
NATURE_INDEX = {"a":0, "b":1, "c":2, "d":3, "s":4}
NATURE = {
        "さみしがり":	[1.1,0.9,1.0,1.0,1.0],
        "いじっぱり":	[1.1,1.0,0.9,1.0,1.0],
        "やんちゃ":	[1.1,1.0,1.0,0.9,1.0],
        "ゆうかん":	[1.1,1.0,1.0,1.0,0.9],
        "ずぶとい":	[0.9,1.1,1.0,1.0,1.0],
        "わんぱく":	[1.0,1.1,0.9,1.0,1.0],
        "のうてんき":	[1.0,1.1,1.0,0.9,1.0],
        "のんき":	[1.0,1.1,1.0,1.0,0.9],
        "ひかえめ":	[0.9,1.0,1.1,1.0,1.0],
        "おっとり":	[1.0,0.9,1.1,1.0,1.0],
        "うっかりや":	[1.0,1.0,1.1,0.9,1.0],
        "れいせい":	[1.0,1.0,1.1,1.0,0.9],
        "おだやか":	[0.9,1.0,1.0,1.1,1.0],
        "おとなしい":	[1.0,0.9,1.0,1.1,1.0],
        "しんちょう":	[1.0,1.0,0.9,1.1,1.0],
        "なまいき":	[1.0,1.0,1.0,1.1,0.9],
        "おくびょう":	[0.9,1.0,1.0,1.0,1.1],
        "せっかち":	[1.0,0.9,1.0,1.0,1.1],
        "ようき":	[1.0,1.0,0.9,1.0,1.1],
        "むじゃき":	[1.0,1.0,1.0,0.9,1.1],
        "てれや":	[1.0,1.0,1.0,1.0,1.0],
        "がんばりや":	[1.0,1.0,1.0,1.0,1.0],
        "すなお":	[1.0,1.0,1.0,1.0,1.0],
        "きまぐれ":	[1.0,1.0,1.0,1.0,1.0],
        "まじめ":	[1.0,1.0,1.0,1.0,1.0],
        "すべて+":	[1.1,1.1,1.1,1.1,1.1],
        "すべて-":	[0.9,0.9,0.9,0.9,0.9],
        }


def calc_nature(up=None, down=None):
    if not up: return "まじめ"
    up = NATURE_INDEX[up]
    down = NATURE_INDEX[down]
    for name, value in NATURE.items():
        if value[up] == 1.1 and value[down] == 0.9:
            return name
        

def is_match(pokemon, move):
    return move.typedata in (t.typedata for t in pokemon.types)


def calc_fire(move, calced_statues, coef=1.0):
    classification = move.classification.name
    if classification == "物理":
        return {"a": calced_statues["a"] * move.power * coef}
    elif classification == "特殊":
        return {"c": calced_statues["c"] * move.power * coef}


def calc_guard(calced_statues, coef=1.0):
    return {"b": calced_statues["h"] * calced_statues["b"] * coef, "d": calced_statues["h"] * calced_statues["d"] * coef}


def _opt_guard(max_value, max_effort, calc_status, calc_guard, target):
    pair = None
    max_result = 0
    for v in range(max_value + 4):
        h = max_effort - v
        if h > 252: continue
        result = calc_guard(calc_status({"h": h, target: v}))[target]
        if max_result < result:
            max_result = result
            pair = {"h": h, target: v}
    return pair, max_result


def opt_guard(max_effort, calc_status, calc_guard, target="all"):
    if target == "b":
        b = 252 if max_effort > 252 else max_effort
        return _opt_guard(b, max_effort if max_effort < 504 else 504, calc_status, calc_guard, "b")
    elif target == "d":
        d = 252 if max_effort > 252 else max_effort
        return _opt_guard(d, max_effort if max_effort < 504 else 504, calc_status, calc_guard, "d")
    elif target == "bd":
        b = 252 if max_effort > 252 else max_effort
        max_result = 0
        pair = None
        for b in range(0, b + 1, 4):
            at = max_effort - b
            d = 252 if at > 252 else at

            for d in range(0, d + 1, 4):
                h = at - d
                if h > 252: continue
                result = calc_guard(calc_status({"h": h, "b": b, "d": d}))
                result = result["b"] + result["d"]
                if max_result < result:
                    max_result = result
                    pair = [{"h": h, "b": b, "d": d}]
                elif max_result == result:
                    pair.append({"h": h, "b": b, "d": d})
        return pair, max_result
    else:
        return {
                "b": opt_guard(max_effort, calc_status, calc_guard, target="b"),
                "d": opt_guard(max_effort, calc_status, calc_guard, target="d"),
                "bd": opt_guard(max_effort, calc_status, calc_guard, target="bd"),
                }

def calc_correction(n):
    if n < 0:
        return 2 / (2 - n)
    else: return 1.0 + 0.5 * n


def calc_coefficient(pokemon, move, rank=0):
    coef = 1.5 if is_match(pokemon, move) else 1.0
    return coef * calc_correction(rank)
# {'b': 132, 'h': 124} ぶるる
# {'b': 252, 'h': 4}　まっし


if __name__ == '__main__':
    from data import *
    from tqdm import tqdm
    p = Pokemons.get(name="マッシブーン")
    nature = "わんぱく"
    s, r = opt_guard(508 - 252, lambda ef: calc_status(p.status[0], ef, nature=nature), calc_guard, target="b")
    s["h"] -= 8
    s["b"] += 8
    print(s)
    s = calc_status(p.status[0], effort=s, nature=nature)
    ef = ["h", "a", "b", "c", "d", "s"]
    for e in ef:
        print(e, s[e])
    print(r, calc_guard(s)["b"])
    # move = Moves.get(name="ブレイブバード")
    # print(calc_fire(move, s, calc_coefficient(p, move, rank=0)))
    # print(calc_guard(s, calc_correction(0)))
    # print(opt_guard(252, lambda ef: calc_status(p.status[0], ef), calc_guard, target="b"))
    # print(sum(calc_guard(s, calc_correction(0)).values()))
    # tmp = 0


    # nature = ""
    # at = 510 - 252
    # results = []
    #
    # for st in tqdm(Statuses.select()):
    #     _, r = opt_guard(at, lambda ef: calc_status(st, ef, nature=nature), calc_guard, target=__import__("sys").argv[1])
    #     results.append((st, r))
    # results.sort(key=lambda x: x[1], reverse=True)
    # for s, r in results:
    #     print(s.pokemon.name, r)
