from subprocess import call
import uuid
from . import MELT_BINARY
from .clip import Clip
from .utils import timestamp

class Composition(object):

    def __init__(self, clips, bgcolor='#000000', singletrack=False, duration=None, fps=30, width=1280, height=720):
        self.clips = clips
        self.bg = bgcolor
        self.singletrack = singletrack
        self.duration = timestamp(duration)
        self.fps = fps
        self.width = width
        self.height = height


    def preview(self):
        call(self.args())


    def preview_xml(self):
        call(self.args() + ['-consumer', 'xml'])


    def save_xml(self, filename=None):
        if filename is None:
            filename = str(uuid.uuid4()) + '.xml'

        call(self.args() + ['-consumer', 'xml:{}'.format(filename)])

        return filename


    def calculate_duration(self):
        pass


    def save(self, filename, **kwargs):
        extra_params = ['{}="{}"'.format(key, val) for key, val in kwargs.items()]
        args = self.args() + ['-consumer', 'avformat:{}'.format(filename)] + extra_params

        if not self.duration:
            self.calculate_duration()

        if self.duration:
            xml = self.save_xml()
            clip = Clip(xml, end=self.duration)
            call(Composition([clip]).args() + args)
        else:
            call(args)

        return filename


    def args(self):
        args = [MELT_BINARY, '-profile', 'atsc_720p_25']

        if not self.singletrack:
            args += ['-track', 'color:{}'.format(self.bg), 'out={}'.format(self.duration)]

        for c in self.clips:
            c.output_fps = self.fps
            args += c.args(self.singletrack)

        if not self.singletrack:
            for i, c in enumerate(self.clips):
                args += ['-transition', 'composite', 'distort=1', 'a_track=0', 'b_track={}'.format(i+1)]

        return args


    def __str__(self):
        return ' '.join(self.args())

