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
        self.mask = None
        self.is_mask = False

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
        '''Duration of the clip'''
        start = self.start if self.start else timestamp(0)
        end = self.end if self.end else timestamp(self.original_duration)
        repeat = self._repeat if self._repeat else 1
        return timestamp((end - start) * repeat)


    @property
    def total_frames(self):
        '''Total frames in the original clip'''
        return self.get_profile().get('total_frames')


    @property
    def original_duration(self):
        '''Duration of the original clip'''
        return self.get_profile().get('duration')


    @property
    def original_fps(self):
        '''FPS of the original clip'''
        return self.get_profile().get('fps')


    @property
    def width(self):
        '''Width of the original clip'''
        return self.get_profile().get('width')


    @property
    def height(self):
        '''Height of the original clip'''
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

        For a full list, see: https://www.mltframework.org/plugins/PluginsTransitions/

        Args:
            name (str): the name of a transition to add
            params (dict): a dictionary containing melt transition parameters
        '''

        self.transitions.append((name, params))
        return self


    def set_mask(self, clip):
        '''
        Sets the mask for the clip based on the luma values of a video, image, or vidpy Clip

        Args:
            clip (Clip or path): any vidpy clip, or path to video or image

        '''

        if isinstance(clip, str):
            clip = Clip(clip)

        clip.is_mask = True
        self.mask = clip

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


    def softglow(self, blur=0.5, brightness=0.75, sharpness=0.85, blurblend=0):
        '''Does softglow effect on highlights

        Args:
            blur (float): Blur of the glow
            brightness (float): Brightness of highlight areas
            sharpness (float): Sharpness of highlight areas
            blurblend (float): lend mode used to blend highlight blur with input image
        '''

        self.fx('frei0r.softglow', {
            '0': blur,
            '1': brightness,
            '2': sharpness,
            '3': blurblend,
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

        Args:
            sequence (list): a sequence of (keyframe, x, w, w, h) params

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


    def crop(self, top=0, left=0, bottom=0, right=0):
        '''Crops the clip

        Args:
            top (int): Pixels to crop from the top
            left (int): Pixels to crop from the left
            bottom (int): Pixels to crop from the bottom
            right (int): Pixels to crop from the right
        '''

        self.fx('crop', {
            'top': top,
            'left': left,
            'bottom': bottom,
            'right': right
        })
        return self


    def position(self, x=0, y=0, w=None, h=None, distort=False):
        '''Positions and resizes the clip. Coordinates can be either in pixels or percent.

        To maintain aspect ration, set distort=False

        Args:
            x: optional x coordinate
            y: optional y coordinate
            w: optional width
            h: optional height
            distort (bool): Option to distort the image or maintain its ratio
        '''

        if w is None:
            w = self.width

        if h is None:
            h = self.height

        self.fx('affine', {
            'transition.rect': '{}/{}:{}x{}'.format(x, y, w, h),
            'transition.valign': 'middle',
            'transition.halign': 'center',
            'transition.fill': 0,
            'transition.distort': 1 if distort else 0,
            'transition.fill': 1 if distort else 0
        })
        return self


    def resize(self, w='100%', h='100%', distort=True):
        '''Resizes the clip. Coordinates can be either in pixels or percent.

        To maintain aspect ration, set distort=False

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


    def brightness(self, brightness=0.5):
        '''
        Adjusts the brightness of the clip

        Args:
            brightness (float): brightness between 0.0 and 1.0

        '''

        self.fx('frei0r.brightness', {'0': brightness})
        return self


    def alpha_op(self, operation='shave', thresh=0.5, amount=0.333344, invert=False, display='image', input_as_alpha=0):
        '''Display and manipulate the alpha channel

        Args:
            display: Display: what to display. Choices are image, alpha_as_gray, gray+red, black, gray, white and checkers.
            input_as_alpha: use input alpha for the display function above.
            operation (str): select the operation to be done on the alpha channel. Options are: shave, shrink_hard, shrink_soft, grow_hard, grow_soft, thresh
            thresh (float): threshold (only used if you've selected the thresh operation)
            amount (float): grow/shrink amount
            invert (bool): invert the alpha channel
        '''

        display = {'image': 1.0/7, 'alpha_as_gray': 2.0/7, 'gray+red': 3.0/7, 'black': 4.0/7, 'gray': 5.0/7, 'white': 6.0/7, 'checkers': 7.0/7}[display]
        operation = {'shave': 1.0/6, 'shrink_hard': 2.0/6, 'shrink_soft': 3.0/6, 'grow_hard': 4.0/6, 'grow_soft': 5.0/6, 'thresh': 6.0/6}.get(operation, operation)

        self.fx('frei0r.alpha0ps', {
            '0': display,
            '1': input_as_alpha,
            '2': operation,
            '3': thresh,
            '4': amount,
            '5': 1 if invert else 0
        })
        return self


    def charcoal(self):
        '''Applies a charcoal effect '''

        self.fx('charcoal')
        return self


    def dust(self, maxdiameter=2, maxcount=10):
        '''Add dust and specks to the clip

        Args:
            maxdiameter (int): Maximal diameter of a dust piece between 0 and 100
            maxcount (int): How many dust pieces are on the image
        '''

        self.fx('dust', {
            'maxdiameter': maxdiameter,
            'maxcount': maxcount
        })
        return self


    def cartoon(self, triplevel=.99, diffspace=0.003):
        '''Cartoonify video, with a form of edge detectection

        Args:
            triplevel (float): level of trip (0 to 1)
            diffspace (float): difference space (0 to 1)
        '''

        self.fx('frei0r.cartoon', {
            '0': triplevel,
            '1': diffspace
        })
        return self


    def contrast(self, amount=0.5):
        '''Adjusts the contrast of the clip

        Args:
            contrast (float): The amount of contrast (between 0 and 1)
        '''

        self.fx('frei0r.contrast0r', {'0': amount})
        return self


    def extract_color(self, color='r'):
        '''Extracts either red, green, or blue from clip

        Args:
            color (str): Either 'r', 'g' or 'b'
        '''

        if color not in 'rgb':
            color = 'r'

        self.fx('frei0r.{}'.format(color.upper()))
        return self


    def vignette(self, aspect=0.5, clear=0, softness=0.6):
        '''Applies a vignette effect

        Args:
            aspect (float): Aspect ratio (0 to 1)
            clear (float): Size of the unaffected center (0 to 1)
            softness (float): Softness (0 to 1)
        '''

        self.fx('frei0r.vignette', {
            '0': aspect,
            '1': clear,
            '2': softness
        })
        return self


    def grain(self, noise=40, contrast=160, brightness=70):
        '''Adds grain over the clip

        Args:
            noise (int): Maximal value of noise (0 to 200)
            contrast (int): Adjust contrast for the image (0 to 400)
            brightness (int): Adjust brightness for the image (0 to 400)
        '''

        self.fx('grain', {
            'noise': noise,
            'contrast': contrast,
            'brightness': brightness
        })
        return self


    def grayscale(self):
        '''Convert the clip to grayscale'''

        self.fx('greyscale')
        return self



    def invert(self):
        '''Inverts the colors of the clip'''

        self.fx('invert')
        return self


    def dynamic_threshold(self):
        '''Applies a dynamic thresholding effect'''

        self.fx('frei0r.twolay0r')
        return self


    def mirror(self, axis='horizontal', reverse=False):
        '''Provides various mirror and image reversing effects.

        Args:
            axis (str): can be either "horizontal", "vertical", "diagonal", "xdiagonal", "flip", or "flop"
            reverse (bool): reverse the mirror

        '''

        self.fx('mirror', {
            'argument': axis,
            'reverse': 1 if reverse else 0
        })
        return self


    def threshold(self, threshold=0.5):
        '''Thresholds the clip

        Args:
            threshold (float): Threshold value (0 to 1)
        '''

        self.fx('frei0r.threshold0r', {'0': threshold})
        return self


    def squareblur(self, size=0.5):
        '''Blurs the clip

        Args:
            size (float): Amount of blur (0 to 1)
        '''

        self.fx('frei0r.squareblur', {'0': size})
        return self


    def sharpness(self, amount=0.3, size=0):
        '''Sharpens the clips
        https://www.mltframework.org/plugins/FilterFrei0r-sharpness/

        Args:
            amount (float): amount
            size (float): size
        '''

        self.fx('frei0r.sharpness', {
            '0': amount,
            '1': size
        })
        return self


    def luminance(self):
        '''Creates a luminance map of the clip'''

        self.fx('frei0r.luminance')
        return self


    def edgeglow(self, threshold=0.5, upscale=0.5, downscale=0):
        '''Adds glowing edges

        Args:
            threshold (float): threshold for edge lightening
            upscale (float): multiplier for upscaling edge brightness
            downscale (float): multiplier for downscaling edge brightness
        '''

        self.fx('frei0r.edgeglow', {
            '0': threshold,
            '1': upscale,
            '2': downscale
        })
        return self


    def gradient(self, start_color='#ffffff', end_color='#000000', pattern='linear', start_opacity=0.5, end_opacity=0.5, start_x=0.5, start_y=0, end_x=0.5, end_y=1, offset=0, blend='normal'):
        '''Draws a gradient on top of the clip.

        Args:
            start_color (str): First color of the gradient
            end_color (str): Second color of the gradient
            pattern (str): "linear" or "radial" gradient
            start_opacity (float): Opacity of the first color of the gradient
            end_opacity (float): Opacity of the second color of the gradient
            start_x (float): X position of the start point of the gradient
            start_y (float): Y position of the start point of the gradient
            end_x (float): X position of the end point of the gradient
            end_y (float): Y position of the end point of the gradient
            offset: Position of first color in the line connecting gradient ends, really useful only for radial gradient
            blend (str): Blend mode. Values can be: 'normal', 'add', 'saturate', 'multiply', 'screen', 'overlay', 'darken', 'lighten', 'colordodge', 'colorburn', 'hardlight', 'softlight', 'difference', 'exclusion', 'hslhue', 'hslsaturation', 'hslcolor', or 'hslluminosity'
        '''

        pattern = {'linear': 'gradient_linear', 'radial': 'gradient_radial'}.get(pattern, 'gradient_linear')

        self.fx('frei0r.cairogradient', {
            '0': pattern,
            '1': start_color,
            '2': start_opacity,
            '3': end_color,
            '4': end_opacity,
            '5': start_x,
            '6': start_y,
            '7': end_x,
            '8': end_y,
            '9': offset,
            '10': blend
        })
        return self


    def hue(self, shift=0):
        '''Adjusts the hue of the clip

        Args:
            shift (float): The amount to shift the hue by (between 0 and 1)
        '''

        self.fx('frei0r.hueshift0r', {'0': shift})
        return self



    def sobel(self):
        '''Applies a sobel filter'''

        self.fx('frei0r.sobel')
        return self


    def posterize(self, levels=0.10):
        '''
        Posterizes the clip by reducing the number of colors used.

        Args:
            levels (float): Number of values per channel
        '''

        self.fx('frei0r.posterize', {'0': levels})
        return self


    def dither(self, amount=0.104167):
        '''Dithers the clip and reduces the number of available colors

        Args:
            amount (float): Number of values per channel
        '''

        self.fx('frei0r.dither', {
            '0': amount
        })
        return self


    def saturate(self, saturation=0.125):
        '''Adjusts the saturation of the clip

        Args:
            saturation (float): Saturation amount (0 to 1)
        '''

        self.fx('frei0r.saturat0r', {'0': saturation})
        return self


    def pixelize(self, width=0.1, height=0.1):
        '''Pixelize the clip

        Args:
            width (float): Horizontal size of one pixel, as percent of screen size (0 to 1)
            height (float): Vertical size of one pixel, as percent of screensize (0 to 1)
        '''

        self.fx('frei0r.pixeliz0r', {
            '0': width,
            '1': height
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
