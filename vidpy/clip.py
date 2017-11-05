from vidpy.utils import timestamp, get_bg_color

class Clip(object):

    def __init__(self, resource=None, service=None, start=0, end=None, offset=0, **kwargs):
        self.resource = resource
        self.service = service
        self.start = timestamp(start)
        self.end = timestamp(end)
        self.offset = timestamp(offset)
        self.repeats = None
        self.output_fps = 30
        self.fxs = []
        self.kwargs = kwargs

        if self.resource.__class__.__name__ == 'Composition':
            self.resource = self.resource.save_xml()
            self._temp_resource = True


    def cut(self, start=None, end=None, duration=None):
        if start:
            self.start = timestamp(start)

        if end:
            self.end = timestamp(end)

        if duration:
            self.end = self.start + timestamp(duration)

        return self


    def set_duration(self, duration):
        self.end = self.start + timestamp(duration)
        return self


    def set_offset(self, offset):
        self.offset = timestamp(offset)
        return self


    def fx(self, name, params=[]):
        '''Adds any melt filter to a clip

        For a full list, see: https://www.mltframework.org/plugins/PluginsFilters/
        '''
        self.fxs.append((name, params))
        return self


    def fadein(self, duration):
        self.fx('brightness', {
            'alpha': '0=0;{}=1'.format(timestamp(duration)),
            'opacity': '0=0;{}=1'.format(timestamp(duration))
        })
        return self


    def fadeout(self, duration):
        self.fx('brightness', {
            'alpha': '{}=1;-1=0'.format(timestamp(duration*-1)),
            'opacity': '{}=1;-1=0'.format(timestamp(duration*-1))
        })
        return self


    def opacity(self, amount):
        self.fx('brightness', {
            'alpha': amount,
            'opacity': amount
        })
        return self


    def chroma(self, amount=0.15, color=None, blend=None):
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

        # self.fx('frei0r.keyspillm0pup', {
        #     '0': color,
        #     '1': '#ffffff',
        #     '2': 1,
        #     '3': 0.5
        # })
        return self


    def rotate(self, amt=1, axis="x"):
        self.fx('affine', {
            'transition.fix_rotate_{}'.format(axis): amt
        })
        return self


    def spin(self, amt=1, axis="x"):
        self.fx('affine', {
            'transition.rotate_{}'.format(axis): amt
        })
        return self


    def glow(self, amount):
        self.fx('frei0r.glow', {
            '0': amount
        })
        return self


    def vflip(self):
        self.fx('avfilter.vflip')
        return self


    def hflip(self):
        self.fx('avfilter.hflip')
        return self


    def flip(self, axis):
        if axis.lower() == 'horizontal':
            self.hflip()
        else:
            self.vflip()
        return self


    def zoompan(self, origin, dest, start=0, end=-1):
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


    def position(self, x=0, y=0, w='100%', h='100%', distort=False):
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
        self.fx('affine', {
            'transition.geometry': '{}/{}:{}x{}'.format(0, 0, w, h),
            'transition.valign': 'middle',
            'transition.halign': 'center',
            'transition.fill': 0,
            'transition.distort': 1 if distort else 0
        })
        return self


    def repeat(self, total):
        self.repeats = total
        return self


    def loop(self):
        self.repeat(100000000)
        return self


    def volume(self, amt):
        self.fx('avfilter.volume', {'av.volume': amt})
        return self


    def args(self, singletrack=False):
        """
        Returns melt command line arguments as a list
        """

        args = []

        if not singletrack:
            args += ['-track']

        if self.offset > 0:
            args += ['-blank', str(self.offset)]

        args += [self.resource, 'in="{}"'.format(self.start)]

        if self.end:
            args += ['out="{}"'.format(self.end)]

        for key in self.kwargs:
            args += ['{}="{}"'.format(key, self.kwargs[key])]

        if self.repeats:
            args += ['-repeat', str(self.repeats)]

        for fx, fxargs in self.fxs:
            if singletrack:
                args += ['-attach-clip', fx]
            else:
                args += ['-attach-track', fx]
                # args += ['-attach-clip', fx]
                # args += ['-attach-cut', fx]
                # args += ['-attach', fx]
            if self.offset > 0:
                args += ['in={}'.format(self.offset)]

            for key in fxargs:
                args += ['{}="{}"'.format(key, str(fxargs[key]))]

        return args


    def __str__(self):
        return ' '.join(self.args())
