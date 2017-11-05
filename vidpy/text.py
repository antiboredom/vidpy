from .clip import Clip

class Text(Clip):
    def __init__(self, text, start=0, end=None, offset=0, color="#ffffff", bgcolor="0x00000000", olcolor="0x00000000", outline=0, halign="center", valign="middle", pad=0, family="Sans", size=1080, style="normal", weight=400, geometry='0/0:100%x100%', **kwargs):

        Clip.__init__(self, 'color:#00000000', start=start, end=end, offset=offset, **kwargs)

        self.fx('dynamictext', {
            'argument': text,
            'geometry': geometry,
            'family': family,
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

