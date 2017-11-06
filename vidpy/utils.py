'''
Utility functions for vidpy
'''

from __future__ import print_function
import os
import sys
from subprocess import call, Popen
import uuid
from PIL import Image
from . import config

def get_bg_color(filename):
    """
    Extracts the top left pixel color from the first frame of a video

    Args:
        filename: an input video

    Returns:
        color
    """

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


def check_melt():
    try:
        devnull = open(os.devnull)
        Popen([config.MELT_BINARY], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print('Error: Could not find melt. See https://antiboredom.github.com/vidpy for installation instructions.')
            sys.exit()


class Frame(int):
    """
    A wrapper class for int to help differentiate between timestamps and frames
    """

    pass


class Second(float):
    """
    A wrapper class for float.

    Allows floats to be converted into melt timestamps
    """

    def __repr__(self):
        return ':%f' % self

    __str__ = __repr__
