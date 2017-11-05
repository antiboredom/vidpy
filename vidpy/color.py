from .clip import Clip

class Color(Clip):
    def __init__(self, color, **kwargs):
        Clip.__init__(self, 'color:{}'.format(color), **kwargs)
