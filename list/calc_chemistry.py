#!/usr/bin/python3

from data import *
import poke_search as ps
import itertools
import random


def create_base(n=1):
    return {x: n for x in OriginTypes.select()}


def calc_atk_chems(*targets):
    atkbase = create_base(0)
    for chem in TypeChemistries.select().where(TypeChemistries.atk << targets):
        atkbase[chem.dfc] = max(atkbase[chem.dfc], chem.effective)
    return atkbase

def calc_dfc_chems(*targets):
    dfcbase = create_base()
    for chem in TypeChemistries.select().where(TypeChemistries.dfc << targets):
        dfcbase[chem.atk] *= chem.effective
    return dfcbase


def calc_anti_atk_chems(*targets):
    return{x: list(TypeChemistries.select().where((TypeChemistries.dfc == x) & (TypeChemistries.effective > 1))) for x in targets}


def calc_anti_dfc_chems(*targets):
    return{x: list(TypeChemistries.select().where((TypeChemistries.atk == x) & (TypeChemistries.effective < 1))) for x in targets}


def type_set(type_combis):
    return [[OriginTypes.get(name=name) for name in x.split()] for x in set([type_join(map(lambda x: x.id, combi)) for combi in type_combis])]


def type_join(ids):
    return " ".join([OriginTypes.get(id=x).name for x in sorted(set(ids))])


class Party:
    def __init__(self, *names):
        self.members = []
        for x in names:
            if x:
                try:
                    self.members.append(Pokemons.get(name=x))
                except: pass

    def add(self, *names):
        for x in names:
            if x:
                try:
                    self.members.append(Pokemons.get(name=x))
                except: pass

    def types(self):
        return [[t.typedata for t in x.types] for x in self.members]

    def ad_list(self):
        atkbase, dfcbase = create_base(0), create_base(2)
        for t in self.types():
            for k, v in calc_atk_chems(*t).items(): atkbase[k] = max(atkbase[k], v)
            for k, v in calc_dfc_chems(*t).items(): dfcbase[k] = min(dfcbase[k], v)
        return atkbase, dfcbase

    def at(self):
        return 6 - len(self.members)


    def calc_ad_anti_list(self):
        atk, dfc = self.ad_list()
        atk_anti_list = list(itertools.chain(*[[x.atk for x in v] for k, v in calc_anti_atk_chems(*[k for k, v in atk.items() if v <= 1]).items()]))

        dfc_anti_list = list(itertools.chain(*[[x.dfc for x in v] for k, v in calc_anti_dfc_chems(*[k for k, v in dfc.items() if v >= 1]).items()]))
        return atk_anti_list, dfc_anti_list

    def ad_suggest(self, anti_list=None):
        if not anti_list:
            anti_list = self.calc_ad_anti_list()
        atk_anti_list, dfc_anti_list = anti_list

        atk_deletes = []
        dfc_deletes = []
        atk_sug = {x: atk_anti_list.count(x) for x in set(atk_anti_list)}
        dfc_sug = {x: dfc_anti_list.count(x) for x in set(dfc_anti_list)}
        for target in itertools.chain(*self.types()):
            try:
                del atk_sug[target]
                deletes.append(target)
                del dfc_sug[target]
                deletes.append(target)
            except: pass
        return sorted(atk_sug.items(), key=lambda x: x[1], reverse=True), sorted(dfc_sug.items(), key=lambda x: x[1], reverse=True)

    def suggest(self, single=False):
        anti_list = self.calc_ad_anti_list()
        atk_anti_list, dfc_anti_list = anti_list
        suggest = set(atk_anti_list) & set(dfc_anti_list)
        if not suggest:
            atk_sug, dfc_sug = self.ad_suggest(anti_list=anti_list)
            suggest = set([x[0] for x in atk_sug] + [x[0] for x in dfc_sug])

        return suggest
    
    def pokemon_suggest(self, sum=0, single=False):
        suggest = self.suggest(single=single)
        sug_list = []
        for sug in itertools.chain(*[itertools.combinations(suggest, x + 1) for x in range(0 if single else 1, 2)[::-1]]):
            sug_list.append([[x.name for x in set(sug)], [x.pokemon.name for x in ps.search(*set(sug), sum=sum)]])
        return sug_list

    def all_analysis(self):
        atk, dfc = self.ad_list()
        chems = []
        for t in itertools.combinations(OriginTypes.select(), 2):
            a = [max(atk[k], v) for k, v in calc_atk_chems(*t).items()]
            d = [min(dfc[k], v) for k, v in calc_dfc_chems(*t).items()]
            chems.append([
                len([x for x in a if x > 1]),
                len([x for x in d if x < 1]),
                [x.name for x in t],
                [x.pokemon.name for x in ps.search(*t)], ])
        max_list = max(chems, key=lambda x: x[0])[0], max(chems, key=lambda x: x[1])[1], (lambda x: x[0] + x[1])(max(chems, key=lambda x: x[0] + x[1]))
        return {"max_list": max_list, "chemistries": chems}

    def __str__(self):
        return ", ".join([x.name for x in self.members])


def random_party(party, sum=0):
    while party.at():
        a = list(itertools.chain(*[x[1] for x in party.pokemon_suggest(sum=sum)]))
        if len(a): party.add(random.choice(list(a)))
        else:
            suggests = party.suggest()
            sug_list = []
            if suggests:
                for suggest in suggests:
                    condition = PokemonTypes.typedata == suggest
                    condition &= Statuses.hp + Statuses.attack + Statuses.block + Statuses.contact + Statuses.defence + Statuses.speed > sum
                    pokemons = [x.pokemon for x in PokemonTypes.select().join(Pokemons).join(Statuses).where(condition).group_by(PokemonTypes.pokemon_id)]
                    sug_list.append(PokemonTypes.select().where(PokemonTypes.pokemon_id << pokemons).group_by(PokemonTypes.pokemon_id).having(fn.Count(PokemonTypes.id) == 2))
            if not sug_list: break
            else:
                name = random.choice(list(itertools.chain(*sug_list))).pokemon.name
                print("bonus add", name, [x.name for x in suggests])
                party.add(name)
    return party


def optimize_random_party(party, sum=0, repeat=5):
    result = random_party(party)
    sug_len = len(result.suggest())
    for i in range(repeat):
        p = random_party(party)
        tmp = len(p.suggest())
        if tmp < sug_len:
            result = p
            sug_len = tmp
    return result


if __name__ == '__main__':
    party = Party("ジバコイル")
    for chem in sorted(party.all_analysis()["chemistries"], key=lambda x: x[1], reverse=True):
        print(chem)
