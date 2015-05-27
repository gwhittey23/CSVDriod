import json
import requests
from requests.exceptions import HTTPError
from urlparse import urljoin
from kivy.logger import Logger
import sys
from kivy.app import App

'cs is used to denote comicstreamer trying to make this plugable between comicstreamer and other servers'
from csvdb.csvdroid_db import add_update_comic, add_series_list
from csvdb.comicsdb_models import *


class ComicStream():

    def __init__(self):
        self.app_config = App.get_running_app()
        self.base_url = self.app_config.config.get('Server', 'url')

        #self.api_key = self.app_config.config.get('Server', 'api_key')

    #get full list from /comiclist from our server

    def get_fulldata(self):
        src = '%s/comiclist' % (self.base_url)
        try:
            r = requests.get(src)
            r.raise_for_status()
        except HTTPError:
            Logger.critical('HTTPerror for %s' % src )
        else:
            data = r.json()
            Logger.debug("get_fulldata started using")
            'brake data into sinle comics'
            for item in data['comics']:
                print item['id']
                comic = CsComic(item)
                add_update_comic(comic)
                #get Thumbnails
        #get Series list
        src = "%s/entities/series" % (self.base_url)
        try:
            r = requests.get(src)
            r.raise_for_status()
        except HTTPError:
            Logger.critical('HTTPerror for %s' % src )
        else:
            print r.json()
            series_list = r.json()
            for item in series_list['series']:
                print item
                if item is not None:
                    add_series_list(item)

class CsSeries(object):
    def __init__(self, comic_data):
        self.id = id
        self.series_name = comic_data['series']
    def get_series_list(self):
        pass

'class representing a single comic'
class CsComic(object):

    def __init__(self, data):
        self.app_config = App.get_running_app()
        self.base_url = self.app_config.config.get('Server', 'url')
        self.base_file = self.app_config.config.get('Server', 'storagedir')
        if isinstance( data, int ):
            self.do_db_setup(data)
        else:
          self.do_json_setup(data)#add just to clean up class
        self.thumb = self._get_cs_thumb()

    def _get_cs_thumb(self):
        print 'get thumb'
        src = "%s/comic/%d/thumbnail" % (self.base_url, int(self.comicstream_number))
        fname='%s/%d_thumb.jpg' %(self.base_file, self.comicstream_number)
        try:
            r = requests.get(src)
            r.raise_for_status()
        except HTTPError:
            Logger.critical('HTTPerror for %s' % src )
        else:
            with open(fname,'w') as f:
                 f.write(r.content)
        return fname
    def do_json_setup(self, data):
        comic_data = data
        self.comicstream_number = comic_data['id']
        self.added_ts = comic_data['added_ts']
        self.month = comic_data['month']
        self.year = comic_data['year']
        self.comments = comic_data['comments']
        self.pubdate = comic_data['date']
        self.issue = comic_data['issue']
        self.page_count = comic_data['page_count']
        self.publisher = comic_data['publisher']
        self.series = comic_data['series']
        self.storyarcs = comic_data['storyarcs']
        self.title = comic_data['title']
        self.volume = comic_data['volume']
        self.weblink = comic_data['weblink']
        self.mod_ts = comic_data['mod_ts']
        self.page_count = comic_data['page_count']
        #self.credits = comic_data['credits']
        #self.characters =  comic_data['characters']
        #self.teams = comic_data['teams']
    def do_db_setup(self, data):
        cscomic = Comics.get(Comics.comicstream_number==data)
        #self.id = cscomic.id
        self.comicstream_number = cscomic.comicstream_number
        self.added_ts = cscomic.added_ts
        self.month = cscomic.month
        self.year = cscomic.year
        self.comments = cscomic.comments
        self.pubdate = cscomic.date
        self.issue = cscomic.issue
        self.page_count = cscomic.page_count
        self.publisher = cscomic.publisher
        self.series = cscomic.series
        self.title = cscomic.title
        self.volume = cscomic.volume
        self.weblink = cscomic.weblink
        self.mod_ts = cscomic.mod_ts
        self.page_count = cscomic.page_count
        self.storyarcs = self.get_storyarks
        #self.characters =  cscomic.characters
        #self.credits = cscomic.credits
 #       self.teams = cscomic.teams

    def get_storyarks(self):
        storyarcs = ComicsStoryarcs.get(comic=self.comicstream_number)
        return storyarcs



def gen_url(server_url,mode):
    api_key ="api_key="
    urljoin(server_url,)

# if __name__ == "__main__":
#     cs_get_comic_info(1860)