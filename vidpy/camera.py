from .clip import Clip

class Camera(Clip):
    '''Captures from a camera using ffmpeg

    tested on mac
    '''

    def __init__(self, device=0, avformat='avfoundation', pixel_format='yuyv422', width=1280, height=720, fps=30, **kwargs):
        params = '{}:{}?framerate={}&video_size={}x{}&pixel_format={}'.format(avformat, device, fps, width, height, pixel_format)
        Clip.__init__(self, params, **kwargs)

