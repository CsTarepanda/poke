from peewee import *
DATABASE = SqliteDatabase("pokemon.sqlite3")
class BaseModel(Model):
    class Meta:
        database = DATABASE


class Origins(BaseModel):
    number = IntegerField(unique=True)
    name = CharField(unique=True)


class Pokemons(BaseModel):
    origin = ForeignKeyField(Origins, related_name="pokemons")
    name = CharField()


class Informations(BaseModel):
    pokemon = ForeignKeyField(Pokemons, related_name="information", unique=True)


class Statuses(BaseModel):
    pokemon = ForeignKeyField(Pokemons, related_name="status", unique=True)
    hp = IntegerField()
    attack = IntegerField()
    block = IntegerField()
    contact = IntegerField()
    defence = IntegerField()
    speed = IntegerField()


class Anothers(BaseModel):
    pokemon = ForeignKeyField(Pokemons, related_name="another", unique=True)
    another_type = CharField(null=True)
    name = CharField(null=True)


class OriginTypes(BaseModel):
    name = CharField(null=True)


class SynonymTypes(BaseModel):
    origin = ForeignKeyField(OriginTypes, related_name="synonym")
    name = CharField(null=True)


class PokemonTypes(BaseModel):
    pokemon = ForeignKeyField(Pokemons, related_name="types")
    typedata = ForeignKeyField(OriginTypes, related_name="pokemons")


class TypeChemistries(BaseModel):
    atk = ForeignKeyField(OriginTypes, related_name="atks")
    dfc = ForeignKeyField(OriginTypes, related_name="dfcs")
    effective = FloatField()


class SkillClassifications(BaseModel):
    name = CharField(unique=True)


# class ZSkills(BaseModel):
#     name = CharField()
#
#
class Skills(BaseModel):
    name = CharField()
    typedata = ForeignKeyField(OriginTypes, related_name="skills");
    classification = ForeignKeyField(SkillClassifications, related_name="skills")
    power = IntegerField(null=True)
    z = IntegerField(null=True)
    pp = IntegerField()
    accuracy = IntegerField(null=True)
    guard = BooleanField()
    direct = BooleanField()
    info = TextField()
    target = CharField()
    

class PokemonSkills(BaseModel):
    classification = CharField()
    pokemon = ForeignKeyField(Pokemons, related_name="skills")
    skill = ForeignKeyField(Skills, related_name="pokemons")


class Abilities(BaseModel):
    name = CharField()
    info = TextField()


class PokemonAbilities(BaseModel):
    pokemon = ForeignKeyField(Pokemons, related_name="abilities")
    ability = ForeignKeyField(Abilities, related_name="pokemons")
    hide = BooleanField(default=False)
#
#
# class Evolution(BaseModel):
#     origin = ForeignKeyField(Pokemon, related_name="evolutions")
#     to = ForeignKeyField(Pokemon, related_name="origin", unique=True)
#     level = IntegerField()
#
#
# class MegaEvolution(BaseModel):
#     origin = ForeignKeyField(Pokemon, related_name="mega_evolution", unique=True)
#     name = CharField(unique=True)
