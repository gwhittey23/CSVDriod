import json
import urllib2
import sys
from kivy.network.urlrequest import UrlRequest
from collections import namedtuple
import pprint
'cs is used to denote comicstream items'



base_url = 'http://192.168.0.8:32500'
class CsSeries(object):
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
        self.thumbnail = self._get_thumb(self.id)

class CsComic(CsSeries):

    def _get_thumb(self, id):
        src = "%s/comic/%d/thumbnail" % (base_url, int(id))
        response=urllib2.urlopen(src)
        fname='../images/%d_thumb.jpg' %id
        with open(fname,'w') as f:
             f.write(response.read())
        return fname
def cs_get_comic_info(comicid):

    src = "%s/comic/%d" % (base_url, int(comicid))
    print src
    response=urllib2.urlopen(src)
    data = json.loads(response.read())
    json_string = json.dumps(data,sort_keys=True,indent=2)
    if not data['total_count'] == '0':
        comic_data = data['comics'][0]
        comic = CsComic(comic_data)
        print comic.thumbnail


if __name__ == "__main__":
    cs_get_comic_info(sys.argv[1])