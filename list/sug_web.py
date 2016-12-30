from bottle import *
from calc_chemistry import Party, random_party, optimize_random_party
from data import Pokemons
from util import *
import itertools

@get('/')
def hello():
    try:
        p = Party(*[request.GET.decode()["poke{}".format(i)] for i in range(6)])
    except Exception as e:
        print(e)
        p = Party()
    if "random_party" in request.GET:
        p = optimize_random_party(p, sum=450, repeat=10)
    return template('index', {
        "autocomplete": [x.name for x in Pokemons.select()],
        "members": p.members,
        "type_suggest": p.suggest(),
        "poke_suggest": p.pokemon_suggest(sum=450),
        })

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
