import os
from subprocess import call, check_output
import uuid
from xml.etree.ElementTree import Element, tostring, fromstring
from . import MELT_BINARY
from .clip import Clip
from .utils import timestamp


class Composition(object):

    def __init__(self, clips, bgcolor='#000000', singletrack=False, duration=None, fps=None, width=None, height=None):
        self.clips = clips
        self.bg = bgcolor
        self.singletrack = singletrack
        self.duration = timestamp(duration)
        self.fps = fps
        self.width = width
        self.height = height


    def xml(self):
        xml = check_output(self.args() + ['-consumer', 'xml'])
        xml = fromstring(xml)

        duration = self.duration

        if not duration:
            duration = self.duration = tractor = xml.find('tractor').get('out')

        xml.find('tractor').set('out', str(duration))
        xml.find('producer').set('out', str(duration))
        xml.find('producer').remove(xml.find('./producer/property[@name="length"]'))
        xml.find('./playlist/entry').set('out', str(duration))

        profile = xml.find('profile')

        if self.fps:
            profile.set('frame_rate_num', str(self.fps))

        if self.width and self.height:
            profile.set('width', str(self.width))
            profile.set('display_aspect_num', str(self.width))
            profile.set('height', str(self.height))
            profile.set('display_aspect_den', str(self.height))

        return tostring(xml)


    def save_xml(self, filename=None):
        if filename is None:
            filename = str(uuid.uuid4()) + '.xml'

        with open(filename, 'wb') as outfile:
            outfile.write(self.xml())

        return filename


    def preview(self):
        xmlfile = self.save_xml()
        call([MELT_BINARY, xmlfile, 'out="{}"'.format(self.duration)])
        os.remove(xmlfile)


    def save(self, filename, **kwargs):
        xmlfile = self.save_xml()

        args = [
            MELT_BINARY,
            xmlfile,
            'out="{}"'.format(self.duration),
            '-consumer',
            'avformat:{}'.format(filename)
        ]

        extra_params = ['{}="{}"'.format(key, val) for key, val in kwargs.items()]
        args += extra_params

        call(args)

        os.remove(xmlfile)

        return filename


    def args(self):
        args = [MELT_BINARY]#, '-profile', 'atsc_720p_30']

        args += ['-track', 'color:{}'.format(self.bg), 'out=0']#.format(self.duration)]

        if self.singletrack:
            args += ['-track']

        for c in self.clips:
            args += c.args(self.singletrack)

        if self.singletrack:
            args += ['-transition', 'composite', 'distort=1', 'a_track=0', 'b_track=1']
        else:
            for i, c in enumerate(self.clips):
                args += ['-transition', 'composite', 'distort=1', 'a_track=0', 'b_track={}'.format(i+1)]

        return args


    def __str__(self):
        return ' '.join(self.args())

