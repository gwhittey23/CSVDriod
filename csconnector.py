import json
import urllib2
from urlparse import urljoin
import logging
import sys
from kivy.network.urlrequest import UrlRequest
from collections import namedtuple
from kivy.uix.settings import SettingsWithSidebar
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
import pprint
'cs is used to denote comicstreamer trying to make this plugable between comicstreamer and other servers'
app_config = App.get_running_app().config
base_url = 'http://192.168.0.8:32500'
base_dir = '/home/gerardwhittey/.config/crdroid/'

class ComicSteam(object):

    def __init__(self):
        self.base_url == app_config('Server', 'url')
        self.api_key == app_config('Server', 'api_key')

    #get full list from /comiclist from our server
    def cs_decode_json(req, results):
        print results

    def get_fulldata(self):

        src = "%s/comiclist" % (base_url)
        req = UrlRequest(
                   'http://api.openweathermap.org/data/2.5/weather?q=Paris,fr',
                    self.cs_decode_json)

    def parseDateStr( self, date_str):
            day = None
            month = None
            year = None
            if  date_str is not None:
                parts = date_str.split('-')
                year = parts[0]
                if len(parts) > 1:
                    month = parts[1]
                    if len(parts) > 2:
                        day = parts[2]
            return day, month, year
class CsSeries(object):
    def __init__(self, comic_data):
        self.id = id
        self.series_name = comic_data['series']

    def get_series_list(self):
        pass

class CsComic(CsSeries):

    def __init__(self, comic_data):
        self.id = id
        self.added_ts = comic_data['added_ts']
        self.characters =  comic_data['characters']
        self.comments = comic_data['comments']
        self.credits = comic_data['credits']
        self.pubdate = comic_data['date']
        self.id = comic_data['id']
        self.issue = comic_data['issue']
        self.page_count = comic_data['page_count']
        self.publisher = comic_data['publisher']
        self.series = comic_data['series']
        self.storyarcs = comic_data['storyarcs']
        self.teams = comic_data['teams']
        self.title = comic_data['title']
        self.volume = comic_data['volume']
        self.weblink = comic_data['weblink']

    def _get_cs_thumb(self, id):
        src = "%s/comic/%d/thumbnail" % (base_url, int(id))
        response=urllib2.urlopen(src)
        fname='%s/%d_thumb.jpg' %(base_dir, id)
        with open(fname,'w') as f:
             f.write(response.read())
        return fname

def cs_get_comic_info(comicid):

    src = "%s/comic/%d" % (base_url, int(comicid))
    logging.debug('src=%s' % src  )
    response=urllib2.urlopen(src)
    data = json.loads(response.read())
    json_string = json.dumps(data,sort_keys=True,indent=2)
    if not data['total_count'] == '0':
        comic_data = data['comics'][0]
        comic = CsComic(comic_data)
        print comic.thumbnail

def gen_url(server_url,mode):
    api_key ="api_key="
    urljoin(server_url,)

# if __name__ == "__main__":
#     cs_get_comic_info(1860)