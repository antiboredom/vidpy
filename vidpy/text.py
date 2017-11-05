from .clip import Clip

class Text(Clip):
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

