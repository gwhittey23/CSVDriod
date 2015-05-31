from kivy.animation import Animation
from kivy.network.urlrequest import UrlRequest
from functools import partial
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from io import BytesIO
 
 
class RemoteImage(Image):
    """
    This class (attempts to) provide an alternative to the Kivy AsyncImage that
    does not glitch when displayed in CAMIScreens.
    """
    remote_source = StringProperty()
    ''' Specifies the URL for the remove image to be downloaded. '''
 
    default_source = StringProperty('graphics/question.png')
    ''' Specifies the image to use if the download fails. '''
 
    _requests = {}
    '''
    In order to prevent duplicate requests for the the same resource, we
    maintain a dictionary tracking what images have been requested, their
    raw data and a list of RemoteImages waiting for the same data. e.g

        {'http://coolness.com/im.png': {'data': '<raw png data>',
                                       {'waiting': [wid1, wid2....]}}
    '''
 
    def __init__(self, **kwargs):
        super(RemoteImage, self).__init__(**kwargs)
 
        # Not sure why, but it seems we have to delay the setting or source for
        # the trophy screens. Setting it immediately gives us a black area
        Clock.schedule_once(lambda dt: self._set_image('graphics/download.png'),
                            False)
        self._start_animation(True)
 
    def _data_arrived(self, req, resp, state):
        """ The data has arrived back from the UrlRequest. """
        if state:
            from kivy.logger import Logger
            Logger.warn("camiasyncimage.py: Download of image failed. "
                        "resp={0}".format(resp))
            Clock.schedule_once(
                lambda dt: self._set_image(self.default_source, True), 0.1)
        else:
            req = RemoteImage._requests[self.remote_source]
            if req['data'] is None:
                # Send the data to the images the are waiting for it
                [img.set_image_data(resp) for img in req['waiting']]
                req['data'] = resp
                req['waiting'] = []
 
            self.set_image_data(resp)
 
    def _set_image(self, source, stop_anim=False):
        """ Set the image source property. """
        self.source = source
        if stop_anim:
            self._stop_animation()
 
    def set_image_data(self, resp):
        """ Set the image data based on the raw data from the webserver. """
        resp = BytesIO(resp)
        self._coreimage = ci = CoreImage(resp,
                                         ext="png",
                                         mipmap=self.mipmap,
                                         anim_delay=self.anim_delay,
                                         keep_data=self.keep_data,
                                         nocache=self.nocache)
        ci.bind(on_texture=self._on_tex_change)
        self.texture = ci.texture
        self._stop_animation()
 
    def _start_animation(self, fade_out):
        """ Start the animation and keep it looping. """
        anim = Animation(opacity=0 if fade_out else 1, duration=0.75)
        anim.bind(on_complete=lambda w, v: self._start_animation(not fade_out))
        anim.start(self)
 
    def _stop_animation(self):
        """ Stop all animation on the widget. """
        Animation.cancel_all(self)
        self.opacity = 1
 
    def on_remote_source(self, widget, value):
        """ Respond to the change of source image. This should be a URL. """
        if value[0:4] == "http":
            req = RemoteImage._requests
            if value in req:
                # The URL has been requested.
                if req[value]['data'] is None:
                    req[value]['waiting'].append(self)
                else:
                    Clock.schedule_once(
                        lambda dt: self.set_image_data(req[value]['data']),
                        0.1)
            else:
                req[value] = {'data': None, 'waiting': []}
                UrlRequest(value,
                           partial(self._data_arrived, state=""),
                           partial(self._data_arrived, state="redirected"),
                           partial(self._data_arrived, state="failed"),
                           partial(self._data_arrived, state="error"))
        else:
            # Delay the call by 0.1 to prevent the initial clock scheduling from
            # interfering.
            Clock.schedule_once(
                lambda dt: self._set_image(self.default_source, True), 0.1)