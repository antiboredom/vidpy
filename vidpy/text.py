from .clip import Clip

class Text(Clip):
    '''Subclass of Clip that allows you to write text in your composition

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

    def __init__(self, text, start=0, end=None, offset=0, color="#ffffff", bgcolor="0x00000000", olcolor="0x00000000", outline=0, halign="center", valign="middle", pad=0, font="Sans", size=1080, style="normal", weight=400, bbox=(0, 0, '100%', '100%'), **kwargs):

        Clip.__init__(self, 'color:#00000000', start=start, end=end, offset=offset, **kwargs)

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

