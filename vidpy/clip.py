import os
from .utils import timestamp, get_bg_color, effects_path, get_melt_profile

class Clip(object):
    '''A VidPy clip

    Args:
        resource (str): Path to a video file, audio file, image, or melt xml document
        service (str): Optional melt service
        start (float): The in-point of the clip in seconds (optional). Setting this will trim from the start of the clip
        end (float): The out-point of the clip in seconds (optional). Setting this will trim from the end of the clip
        offset (float): Time in seconds before the clip is played.
        **kwargs: Option parameters that will get sent to melt
    '''

    def __init__(self, resource=None, service=None, start=0, end=None, offset=0, **kwargs):
        self.resource = resource
        self.service = service
        self.start = timestamp(start)
        self.end = timestamp(end)
        self.offset = timestamp(offset)
        self._repeat = None
        self.output_fps = 30
        self._speed = 1.0
        self.fxs = []
        self.transitions = []
        self.kwargs = kwargs
        self.__profile = None

        if self.resource.__class__.__name__ == 'Composition':
            self.resource = self.resource.save_xml()
            self._temp_resource = True


    def get_profile(self):
        '''Returns the melt generated profile for the clip'''
        if self.__profile is None:
            self.__profile = get_melt_profile(self.resource)
        return self.__profile

    @property
    def duration(self):
        '''User defined duration'''
        start = self.start if self.start else timestamp(0)
        end = self.end if self.end else timestamp(self.original_duration)
        return timestamp(end - start)

    @property
    def total_frames(self):
        '''Gets the duration and caches it'''
        return self.get_profile().get('total_frames')

    @property
    def original_duration(self):
        '''Gets the duration and caches it'''
        return self.get_profile().get('duration')

    @property
    def original_fps(self):
        return self.get_profile().get('fps')

    @property
    def width(self):
        return self.get_profile().get('width')

    @property
    def height(self):
        return self.get_profile().get('height')


    def cut(self, start=None, end=None, duration=None):
        '''Trims the clip

        Args:
            start (float): Time to trim from the start of the clip in seconds
            end (float): Time to trim from the end of the clip in seconds
            duration (float): Total duration of the clip (overwrited end)

        '''

        if start:
            self.start = timestamp(start)

        if end:
            self.end = timestamp(end)

        if duration:
            self.end = self.start + timestamp(duration)

        return self


    def set_duration(self, duration):
        '''Sets the duration of the clip

        Args:
            duration (float): Duration of the clip in seconds
        '''

        self.end = self.start + timestamp(duration)
        return self


    def set_offset(self, offset):
        '''Sets the offset of the clip - determines when the clip will start playing.

        Args:
            offset (float): Offset of the clip in seconds
        '''

        self.offset = timestamp(offset)
        return self


    def speed(self, speed):
        '''Sets the playback speed of the clip.

        The speed can be any number between 20 and 0.01.
        Negative values will play video in reverse.

        Args:
            speed (float): playback speed
        '''

        self._speed = speed
        return self


    def fx(self, name, params=None):
        '''Adds any melt filter to a clip

        For a full list, see: https://www.mltframework.org/plugins/PluginsFilters/

        Args:
            name (str): the name of a filter to add
            params (dict): a dictionary containing melt filter parameters
        '''

        if params is None:
            params = []

        self.fxs.append((name, params))
        return self



    def transition(self, name, params=None):
        '''Adds any melt transition to a track

        For a full list, see: https://www.mltframework.org/plugins/PluginsFilters/

        Args:
            name (str): the name of a filter to add
            params (dict): a dictionary containing melt filter parameters
        '''

        self.transitions.append((name, params))
        return self


    def luma(self, start=None, end=None):
        self.transition('luma', {'in': timestamp(start), 'out': timestamp(end)})
        return self


    def fadein(self, duration):
        '''Fades the clip in

        Args:
            duration (float): Time to fade in, in seconds
        '''

        self.fx('brightness', {
            'alpha': '0=0;{}=1'.format(timestamp(duration)),
            'opacity': '0=0;{}=1'.format(timestamp(duration))
        })
        return self


    def fadeout(self, duration):
        '''Fades the clip out

        Args:
            duration (float): Time to fade out, in seconds
        '''

        self.fx('brightness', {
            'alpha': '{}=1;-1=0'.format(timestamp(duration*-1)),
            'opacity': '{}=1;-1=0'.format(timestamp(duration*-1))
        })
        return self


    def opacity(self, amount):
        '''Sets the clip's opacity

        Args:
            amount (float): Opacity, between 0.0 and 1.0
        '''

        self.fx('brightness', {
            'alpha': amount,
            'opacity': amount
        })
        return self


    def chroma(self, amount=0.15, color=None, blend=None):
        '''Removes a color from the clip, making it transparent

        Args:
            amount (float): distance to the color, between 0.0 and 1.0. The higher the number the more will be removed.
            color (str): The color to remove. If left blank, the top left pixel color will be used.
            blend (float): Chromakey blend value, between 0 and 1
        '''

        if color is None:
            color = get_bg_color(self.resource)

        if blend:
            self.fx('avfilter.chromakey', {
                'av.color': color,
                'av.similarity': amount,
                'av.blend': blend
            })
        else:
            self.fx('frei0r.bluescreen0r', {
                '0': color,
                '1': amount
            })

        return self


    def rotate(self, amount=1, axis="x"):
        '''Rotate the clip along an axis

        Args:
            amount (float): Degrees to rotate by
            axis (str): The axis to rotate over, by default "x"
        '''

        self.fx('affine', {
            'transition.fix_rotate_{}'.format(axis): amount
        })
        return self


    def spin(self, speed=1, axis="x"):
        '''Spin the clip continuously. But why?

        Args:
            speed (float): Speed to rotate by
            axis (str): The axis to rotate over, by default "x"
        '''

        self.fx('affine', {
            'transition.rotate_{}'.format(axis): speed
        })
        return self


    def blink(self, interval):
        '''Blinks the clip at an interval

        Args:
            interval (float): time in seconds for on/off cycle
        '''

        self.transition('webvfx', {
            'resource': effects_path('blink.html'),
            'interval': interval * 1000,
        })

        return self


    def glow(self, blur=0.5):
        '''Apply a glow effect

        Args:
            blur (float): Amount to blur by
        '''

        self.fx('frei0r.glow', {
            '0': blur
        })
        return self


    def vflip(self):
        '''Flip the clip vertically'''

        self.fx('avfilter.vflip')
        return self


    def hflip(self):
        '''Flip the clip horizontally'''

        self.fx('avfilter.hflip')
        return self


    def flip(self, axis):
        '''Flip the clip over an axis

        Args:
            axis (str): The axis to flip over, either "horizontal" or "vertical"
        '''

        if axis.lower() == 'horizontal':
            self.hflip()
        else:
            self.vflip()
        return self


    def move(self, sequence, repeat=False, cycle=0, mirror=False):
        '''Moves the clip around.

        Takes a list of (keyframe, x, y, w, h) params
        At each target frame, the clip will be moved and optionally resized
        to the supplied x,y,w,h params.

        You can use pixels or percentages (in quotes)
        '''

        args = ['{}={}/{}:{}x{}'.format(*s) for s in sequence]
        args = ';'.join(args)
        self.fx('affine', {
            'transition.geometry': args,
            'background': 'color:0',
            'transition.repeat_off': 0 if repeat else 1,
            'transition.cycle': cycle,
            'transition.mirror': 1 if mirror else 0
        })
        return self


    def zoompan(self, origin, dest, start=0, end=-1):
        '''Zooms and pans the clip over time

        Takes an origin and destination coordinates either in pixels or percent.

        Args:
            origin (list): where to start from, as an [x, y, width, height] list
            dest (list): where to end up as an [x, y, width, height] list
            start (float): when to start the zoompan in seconds
            end (float): when to end the zoompan in seconds
        '''

        args = {
            'x1': origin[0],
            'y1': origin[1],
            'w1': origin[2],
            'h1': origin[3],
            'x2': dest[0],
            'y2': dest[1],
            'w2': dest[2],
            'h2': dest[3],
            'start': start,
            'end': end
        }
        self.fx('affine', {
            'transition.geometry': '{start}={x1}/{y1}:{w1}x{h1};{end}={x2}/{y2}:{w2}x{h2}'.format(**args),
            'background': 'colour:0'
        })
        return self


    def text(self, text, color="#ffffff", bgcolor="0x00000000", olcolor="0x00000000", outline=0, halign="center", valign="middle", pad=0, font="Sans", size=1080, style="normal", weight=400, bbox=(0, 0, '100%', '100%')):
        '''Overlays text on a clip.

        Args:
            text (str): The text
            font (str): The font family to use
            color (str): Text foreground color
            bgcolor (str): Optional background color
            olcolor (str): Text outline color
            outline (int): Outline size
            style (str): Font style, can be "normal" or "italic"
            weight (int): The weight of the text (boldness). Can be between 100 and 1000
            bbox (list): A bounding box for text to appear in. By default is (0, 0, '100%', '100%'
            halign (str): Horizontal aligment of text. Can be "center" (default), "left" or "right"
            valign (str): Vertical aligment of text. Can be "middle" (default), "top" or "bottom"

        '''

        geometry = '{}/{}:{}x{}'.format(*bbox)

        self.fx('dynamictext', {
            'argument': text,
            'geometry': geometry,
            'family': font,
            'size': size,
            'weight': weight,
            'style': style,
            'fgcolour': color,
            'bgcolour': bgcolor,
            'olcolour': olcolor,
            'outline': outline,
            'pad': pad,
            'halign': halign,
            'valign': valign
        })

        return self


    def position(self, x=0, y=0, w='100%', h='100%', distort=False):
        '''Positions and resizes the clip. Coordinates can be either in pixels or percent.

        Aspect ratio will be mainted unless distort is set to True

        Args:
            x: optional x coordinate
            y: optional y coordinate
            w: optional width
            h: optional height
            distort (bool): Option to distort the image or maintain its ratio
        '''

        self.fx('affine', {
            'transition.geometry': '{}/{}:{}x{}'.format(x, y, w, h),
            'transition.valign': 'middle',
            'transition.halign': 'center',
            'transition.fill': 0,
            'transition.distort': 1 if distort else 0,
            'transition.fill': 1 if distort else 0
        })
        return self


    def resize(self, w='100%', h='100%', distort=False):
        '''Resizes the clip. Coordinates can be either in pixels or percent.

        Aspect ratio will be mainted unless distort is set to True

        Args:
            w: optional width
            h: optional height
            distort (bool): Option to distort the image or maintain its ratio
        '''

        self.fx('affine', {
            'transition.geometry': '{}/{}:{}x{}'.format(0, 0, w, h),
            'transition.valign': 'middle',
            'transition.halign': 'center',
            'transition.fill': 0,
            'transition.distort': 1 if distort else 0
        })
        return self


    def repeat(self, total):
        '''Repeats the clip

        Args:
            total (int): How many times to repeat the clip
        '''

        self._repeat = total
        return self


    def loop(self):
        '''Loops the clip indefinitely'''

        self.repeat(100000000)
        return self


    def volume(self, amt):
        '''Sets the volume for the clip, from 0 (mute) to 1 (full volume)

        Args:
            amt (float): Volume between 0 and 1
        '''

        self.fx('avfilter.volume', {'av.volume': amt})
        return self


    def args(self, singletrack=False):
        '''Returns melt command line arguments as a list'''

        args = []

        if not singletrack:
            args += ['-track']

        if self.offset > 0:
            args += ['-blank', str(self.offset)]

        resource = self.resource

        if self._speed != 1.0:
            resource = 'timewarp:{}:{}'.format(self._speed, resource)

        args += [resource, 'in="{}"'.format(self.start)]

        if self.end:
            args += ['out="{}"'.format(self.end)]

        for key in self.kwargs:
            args += ['{}="{}"'.format(key, self.kwargs[key])]

        if self._repeat:
            args += ['-repeat', str(self._repeat)]

        for fx, fxargs in self.fxs:
            if singletrack:
                args += ['-attach-clip', fx]
            else:
                args += ['-attach-track', fx]
            if self.offset > 0:
                args += ['in={}'.format(self.offset)]

            for key in fxargs:
                args += ['{}="{}"'.format(key, str(fxargs[key]))]

        return args


    def transition_args(self, track_number):
        args = []
        for transition, targs in self.transitions:
            args += ['-transition', transition]
            for key in targs:
                args += ['{}="{}"'.format(key, str(targs[key]))]
            args += ['a_track=0', 'b_track={}'.format(track_number)]
        return args


    def preview(self):
        '''Previews the clip'''

        from vidpy import Composition
        comp = Composition([self])
        comp.preview()


    def save(self, filename, **kwargs):
        '''Saves the clip as a video file

        Args:
            filename (str): The file to save to.
            kwargs: Pass in any arguments that you would to Composition (width, height, fps, bgcolor)
        '''

        from vidpy import Composition
        comp = Composition([self], **kwargs)
        comp.save(filename)


    def __str__(self):
        return ' '.join(self.args())
