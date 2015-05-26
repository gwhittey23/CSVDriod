from peewee import *

database = SqliteDatabase('comics.db', **{})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class Characters(BaseModel):
    name = UnknownField(null=True, unique=True)  # VARCHAR

    class Meta:
        db_table = 'characters'

class Comics(BaseModel):
    added_ts = DateTimeField(null=True)
    comments = UnknownField(null=True)  # VARCHAR
    date = DateTimeField(null=True)
    day = IntegerField(null=True)
    deleted_ts = DateTimeField(null=True)
    file = UnknownField(null=True)  # VARCHAR
    filesize = IntegerField(null=True)
    folder = UnknownField(null=True)  # VARCHAR
    hash = UnknownField(null=True)  # VARCHAR
    imprint = UnknownField(null=True)  # VARCHAR
    issue = UnknownField(null=True)  # VARCHAR
    issue_num = UnknownField(null=True)  # FLOAT
    lastread_page = IntegerField(null=True)
    lastread_ts = DateTimeField(null=True)
    mod_ts = DateTimeField(null=True)
    month = IntegerField(null=True)
    page_count = IntegerField(null=True)
    path = UnknownField(null=True, unique=True)  # VARCHAR
    publisher = UnknownField(null=True)  # VARCHAR
    series = UnknownField(null=True)  # VARCHAR
    title = UnknownField(null=True)  # VARCHAR
    volume = IntegerField(null=True)
    weblink = UnknownField(null=True)  # VARCHAR
    year = IntegerField(null=True)

    class Meta:
        db_table = 'comics'

class ComicsCharacters(BaseModel):
    character = ForeignKeyField(db_column='character_id', null=True, rel_model=Characters, to_field='id')
    comic = ForeignKeyField(db_column='comic_id', null=True, rel_model=Comics, to_field='id')

    class Meta:
        db_table = 'comics_characters'

class Generictags(BaseModel):
    name = UnknownField(null=True, unique=True)  # VARCHAR

    class Meta:
        db_table = 'generictags'

class ComicsGenerictags(BaseModel):
    comic = ForeignKeyField(db_column='comic_id', null=True, rel_model=Comics, to_field='id')
    generictags = ForeignKeyField(db_column='generictags_id', null=True, rel_model=Generictags, to_field='id')

    class Meta:
        db_table = 'comics_generictags'

class Genres(BaseModel):
    name = UnknownField(null=True, unique=True)  # VARCHAR

    class Meta:
        db_table = 'genres'

class ComicsGenres(BaseModel):
    comic = ForeignKeyField(db_column='comic_id', null=True, rel_model=Comics, to_field='id')
    genre = ForeignKeyField(db_column='genre_id', null=True, rel_model=Genres, to_field='id')

    class Meta:
        db_table = 'comics_genres'

class Locations(BaseModel):
    name = UnknownField(null=True, unique=True)  # VARCHAR

    class Meta:
        db_table = 'locations'

class ComicsLocations(BaseModel):
    comic = ForeignKeyField(db_column='comic_id', null=True, rel_model=Comics, to_field='id')
    location = ForeignKeyField(db_column='location_id', null=True, rel_model=Locations, to_field='id')

    class Meta:
        db_table = 'comics_locations'

class Storyarcs(BaseModel):
    name = UnknownField(null=True, unique=True)  # VARCHAR

    class Meta:
        db_table = 'storyarcs'

class ComicsStoryarcs(BaseModel):
    comic = ForeignKeyField(db_column='comic_id', null=True, rel_model=Comics, to_field='id')
    storyarc = ForeignKeyField(db_column='storyarc_id', null=True, rel_model=Storyarcs, to_field='id')

    class Meta:
        db_table = 'comics_storyarcs'

class Teams(BaseModel):
    name = UnknownField(null=True, unique=True)  # VARCHAR

    class Meta:
        db_table = 'teams'

class ComicsTeams(BaseModel):
    comic = ForeignKeyField(db_column='comic_id', null=True, rel_model=Comics, to_field='id')
    team = ForeignKeyField(db_column='team_id', null=True, rel_model=Teams, to_field='id')

    class Meta:
        db_table = 'comics_teams'

class Persons(BaseModel):
    name = UnknownField(null=True, unique=True)  # VARCHAR

    class Meta:
        db_table = 'persons'

class Roles(BaseModel):
    name = UnknownField(null=True, unique=True)  # VARCHAR

    class Meta:
        db_table = 'roles'

class Credits(BaseModel):
    comic = ForeignKeyField(db_column='comic_id', rel_model=Comics, to_field='id')
    person = ForeignKeyField(db_column='person_id', rel_model=Persons, to_field='id')
    role = ForeignKeyField(db_column='role_id', rel_model=Roles, to_field='id')

    class Meta:
        db_table = 'credits'
        primary_key = CompositeKey('comic', 'person', 'role')


import sys

for cls in sys.modules[__name__].__dict__.values():
    try:
        if BaseModel in cls.__bases__:
            cls.create_table()
    except:
        pass