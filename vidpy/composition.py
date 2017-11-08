import os
from subprocess import call, check_output
import uuid
from xml.etree.ElementTree import Element, tostring, fromstring
from . import config
from .clip import Clip
from .utils import timestamp, check_melt


class Composition(object):
    '''A composition made of a list of clips.

    Args:
        clips (list): A list of Clip objects

        bgcolor (str): The background color of the composition, in hex

        singletrack (bool): Boolean that determines if clips play all at once (default) or sequentially

        duration (float): Duration of the composition in seconds.

        fps (int): Frames per second of output

        width (int): Width of output in pixels

        height (int): Height of output in pixels
    '''

    def __init__(self, clips, bgcolor='#000000', singletrack=False, duration=None, fps=None, width=None, height=None):
        self.clips = clips
        self.bg = bgcolor
        self.singletrack = singletrack
        self.duration = timestamp(duration)
        self.fps = fps
        self.width = width
        self.height = height


    def autoset_duration(self, xml):
        duration = self.duration

        if not duration:
            duration = self.duration = xml.find('tractor').get('out')

        xml.find('tractor').set('out', str(duration))
        xml.find('producer').set('out', str(duration))
        xml.find('producer').remove(xml.find('./producer/property[@name="length"]'))
        xml.find('./playlist/entry').set('out', str(duration))

        return xml


    def set_meta(self, xml):
        profile = xml.find('profile')

        if self.fps:
            profile.set('frame_rate_num', str(self.fps))

        if self.width and self.height:
            profile.set('width', str(self.width))
            profile.set('display_aspect_num', str(self.width))
            profile.set('height', str(self.height))
            profile.set('display_aspect_den', str(self.height))

        return xml


    def xml(self):
        '''Renders the composition as XML and sets the current duration, width, height and fps.

        Returns:
            str: an mlt xml representation of the composition
        '''

        xml = check_output(self.args() + ['-consumer', 'xml'])
        xml = fromstring(xml)

        xml = self.autoset_duration(xml)
        xml = self.set_meta(xml)

        return tostring(xml)


    def save_xml(self, filename=None):
        '''Saves the composition as a mlt xml file.

        Args:
            filename (str): path to save to

        Returns:
            str: path to the saved file

        '''

        if filename is None:
            filename = str(uuid.uuid4()) + '.xml'

        with open(filename, 'wb') as outfile:
            outfile.write(self.xml())

        return filename


    def preview(self):
        ''' Previews the composition using melt's default viewer.'''

        check_melt()

        xmlfile = self.save_xml()
        call([config.MELT_BINARY, xmlfile, 'out="{}"'.format(self.duration)])
        os.remove(xmlfile)


    def save(self, filename, **kwargs):
        '''Save the composition as a video file.

        Args:
            filename (str): the file to save to (any video type is accepted)
            **kwargs: additional parameters to pass to ffmpeg

        Returns:
            filename (str): the path to the saved file

        '''

        check_melt()

        xmlfile = self.save_xml()

        args = [
            config.MELT_BINARY,
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
        '''Generate mlt command line arguments

        Returns:
            str: mlt command line arguments
        '''

        args = [config.MELT_BINARY]


        # add the the background track
        args += ['-track', 'color:{}'.format(self.bg), 'out=0']

        # add a track for all clips in singletrack
        if self.singletrack:
            args += ['-track']

        # add args and transitions for all clips
        for i, c in enumerate(self.clips):
            args += c.args(self.singletrack)
            args += c.transition_args(i+1)

        # add composite transitions for all tracks
        if self.singletrack:
            args += ['-transition', 'composite', 'distort=1', 'a_track=0', 'b_track=1']
        else:
            for i, c in enumerate(self.clips):
                args += ['-transition', 'composite', 'distort=1', 'a_track=0', 'b_track={}'.format(i+1)]
                args += ['-transition', 'mix', 'a_track=0', 'b_track={}'.format(i+1)]

        return args


    def __str__(self):
        return ' '.join(self.args())

