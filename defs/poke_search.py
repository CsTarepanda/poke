#!/usr/bin/python3

from data import *

def search(*types, h=0, a=0, b=0, c=0, d=0, s=0, sum=0, cstm=None):
    condition = PokemonTypes.typedata << types
    if h: condition &= Statuses.hp > h
    if a: condition &= Statuses.attack > a
    if b: condition &= Statuses.block > b
    if c: condition &= Statuses.contact > c
    if d: condition &= Statuses.defence > d
    if s: condition &= Statuses.speed > s
    if sum: condition &= Statuses.hp + Statuses.attack + Statuses.block + Statuses.contact + Statuses.defence + Statuses.speed > sum
    if cstm: condition &= cstm(Statuses)
    return PokemonTypes.select().join(Pokemons).join(Statuses).where(condition).group_by(PokemonTypes.pokemon_id).having(fn.Count(PokemonTypes.id) == 2) if len(types) == 2 else PokemonTypes.select().join(Pokemons).join(Statuses).group_by(PokemonTypes.pokemon_id).having((fn.Count(PokemonTypes.id) == 1) & condition)

if __name__ == '__main__':
    for x in search(*[SynonymTypes.get(name=x).origin for x in input().split()]): print(x.pokemon.name)
