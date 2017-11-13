from .clip import Clip

class Color(Clip):
    '''Subclass of Clip to create solid colors

    Args:
        color (str): the color of the clip

    '''

    def __init__(self, color, **kwargs):
        Clip.__init__(self, 'color:{}'.format(color), **kwargs)
