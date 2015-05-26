import json
import urllib2
from urlparse import urljoin
from kivy.logger import Logger
import sys
from kivy.network.urlrequest import UrlRequest
from collections import namedtuple
from kivy.uix.settings import SettingsWithSidebar
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
import pprint
'cs is used to denote comicstreamer trying to make this plugable between comicstreamer and other servers'
from csvdb.csvdroid_db import add_update_comic, build_db
base_url = 'http://192.168.0.8:32500'
base_dir = '/home/gerardwhittey/.config/crdroid/'

class ComicStream():

    def __init__(self):
        self.app_config = App.get_running_app()
        self.base_url = self.app_config.config.get('Server', 'url')
        #self.api_key = self.app_config.config.get('Server', 'api_key')

    #get full list from /comiclist from our server

    def get_fulldata(self):
        src = "%s/comiclist?storyarc=Secret+Invasion" % (self.base_url)
        response=urllib2.urlopen(src)
        data = json.loads(response.read())
        Logger.debug("get_fulldata started using")
        Logger.debug(src)

        'brake data into sinle comics'
        for item in data['comics']:
            print item['id']
            single_comic = CsComic(item)
            add_update_comic(single_comic)


class CsSeries(object):
    def __init__(self, comic_data):
        self.id = id
        self.series_name = comic_data['series']
    def get_series_list(self):
        pass

class CsComic(object):

    def __init__(self, comic_data):
        self.comicstream_number = comic_data['id']
        self.added_ts = comic_data['added_ts']
        self.month = comic_data['month']
        self.year = comic_data['year']
        self.characters =  comic_data['characters']
        self.comments = comic_data['comments']
        self.credits = comic_data['credits']
        self.pubdate = comic_data['date']
        self.issue = comic_data['issue']
        self.page_count = comic_data['page_count']
        self.publisher = comic_data['publisher']
        self.series = comic_data['series']
        self.storyarcs = comic_data['storyarcs']
        self.teams = comic_data['teams']
        self.title = comic_data['title']
        self.volume = comic_data['volume']
        self.weblink = comic_data['weblink']
        self.mod_ts = comic_data['mod_ts']

    def _get_cs_thumb(self):
        src = "%s/comic/%d/thumbnail" % (base_url, int(self.comicstream_number))
        response=urllib2.urlopen(src)
        fname='%s/%d_thumb.jpg' %(base_dir, self.comicstream_number)
        with open(fname,'w') as f:
             f.write(response.read())
        return fname

def cs_get_comic_info(comicid):

    src = "%s/comic/%d" % (base_url, int(comicid))
    Logger.debug('src=%s' % src  )
    response=urllib2.urlopen(src)
    data = json.loads(response.read())
    json_string = json.dumps(data,sort_keys=True,indent=2)
    if not data['total_count'] == '0' and not int(data['total_count' ])> 1:
        comic_data = data['comics'][0]
        comic = CsComic(comic_data)

def gen_url(server_url,mode):
    api_key ="api_key="
    urljoin(server_url,)

# if __name__ == "__main__":
#     cs_get_comic_info(1860)