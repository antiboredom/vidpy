'''
Utility functions for vidpy
'''

from __future__ import print_function
import os
import sys
from subprocess import call, Popen, check_output
from xml.etree.ElementTree import fromstring
import uuid
from PIL import Image
from . import config

def get_bg_color(filename):
    '''
    Extracts the top left pixel color from the first frame of a video

    Args:
        filename: an input video

    Returns:
        color
    '''

    tempname = str(uuid.uuid4()) + '.png'
    call([
        'ffmpeg',
        '-hide_banner',
        '-loglevel', 'panic',
        '-i', filename,
        '-t', '1',
        '-f', 'image2',
        '-y',
        tempname
    ])
    image = Image.open(tempname)
    red, green, blue = image.getpixel((0, 0))
    color = '#%02x%02x%02x' % (red, green, blue)
    os.remove(tempname)
    return color


def timestamp(val):
    '''
    Converts a value to a frame or a Second
    '''

    if val is None:
        return None
    elif val.__class__.__name__ == 'Frame':
        return val
    else:
        return Second(val)


def get_melt_profile(resource):
    '''
    Retrieves a melt profile from any given resource.

    Inlcudes, with, height, fps, duration
    '''

    xml = check_output([config.MELT_BINARY, resource, '-consumer', 'xml'])
    xml = fromstring(xml)
    profile = xml.find('profile')
    total_frames = int(xml.find('producer').find('property[@name="length"]').text)
    fps = float(profile.get('frame_rate_num'))/float(profile.get('frame_rate_den'))
    width = int(profile.get('width'))
    height =  int(profile.get('height'))
    duration = round(float(total_frames)/fps, 2)
    profile = {
        'total_frames': total_frames,
        'fps': fps,
        'width': width,
        'height': height,
        'duration': duration
    }
    return profile


def check_melt():
    '''
    Checks for a melt installation
    '''

    try:
        devnull = open(os.devnull)
        Popen([config.MELT_BINARY], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print('Error: Could not find melt. See https://antiboredom.github.com/vidpy for installation instructions.')
            sys.exit()


def effects_path(effect=None):
    '''Returns the path to the effects directory'''

    returnpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'effects')

    if effect is not None:
        returnpath = os.path.join(returnpath, effect)

    return returnpath


class Frame(int):
    '''A wrapper class for int to help differentiate between timestamps and frames'''

    pass


class Second(float):
    '''
    A wrapper class for float.

    Allows floats to be converted into melt timestamps
    '''

    def __repr__(self):
        return ':%f' % self

    def __add__(self, y):
        return Second(float(self) + y)

    def __sub__(self, y):
        return Second(float(self) - y)

    def __mul__(self, y):
        return Second(float(self) * y)

    def __floordiv__(self, y):
        return Second(float(self) // y)

    def __mod__(self, y):
        return Second(float(self) % y)

    def __div__(self, y):
        return Second(float(self) / y)

    def __truediv__(self, y):
        return Second(float(self) / y)

    __str__ = __repr__
