__author__ = 'gerardwhittey'

from peewee import *
from kivy.logger import Logger
from comicsdb_models import *


def add_update_comic(cls):
    try:
        with database.atomic():
            return Comics.create(
                comicstream_number=cls.comicstream_number,
                added_ts=cls.added_ts,
                comments=cls.comments,
                date=cls.pubdate,
                issue=cls.issue,
                page_count=cls.page_count,
                publisher=cls.publisher,
                series=cls.series,
                #teams=cls.teams,
                title=cls.title,
                volume=cls.volume,
                mod_ts = cls.mod_ts,
                month = cls.month,
                year=cls.year,
                weblink=cls.weblink)
    except IntegrityError:
        new_comic = Comics.get(Comics.comicstream_number == cls.comicstream_number)
        new_comic.added_ts=cls.added_ts
        new_comic.comments=cls.comments
        new_comic.date=cls.pubdate
        new_comic.issue=cls.issue
        new_comic.page_count=cls.page_count
        new_comic.publisher=cls.publisher
        new_comic.series=cls.series
        #new_comic.teams=cls.teams
        new_comic.title=cls.title
        new_comic.volume=cls.volume
        new_comic.mod_ts = cls.mod_ts
        new_comic.month = cls.month
        new_comic.year=cls.year
        new_comic.weblink=cls.weblink
        new_comic.save()

    if not cls.storyarcs == None:
        print 'story arcs : %s' % cls.storyarcs
        add_story_arcs(new_comic.id,cls.storyarcs)
        Logger.debug('started story %s' %cls.storyarcs)
def add_story_arcs(id, storyarcs):
    print 'storyarc'
    for story in storyarcs:
        new_story, created = Storyarcs.get_or_create(name=story)
        acomic = Comics.get(Comics.id==id)
        new_comicarc, ns_created = ComicsStoryarcs.get_or_create(comic=acomic.id,storyarc=new_story.id)

def build_db():
    # try:
    #     drop_all_tables()
    # except:
    #     Logger.info('somethin happened in drop_all_tables')

    try:
        create_all_tables()
    except:
        Logger.info('somethin happened in create_all_tables')

    import sys
    Logger.info('Start db rebuild')


def drop_all_tables():
    import sys
    for cls in sys.modules[__name__].__dict__.values():
        try:
            if BaseModel in cls.__bases__:
                cls.drop_table()
        except:
            pass
def create_all_tables():
    import sys
    Logger.info('Start db rebuild')
    for cls in sys.modules[__name__].__dict__.values():
        try:
            if BaseModel in cls.__bases__:
                cls.create_table()
        except:
            pass