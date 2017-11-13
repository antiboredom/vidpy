from .clip import Clip

class Camera(Clip):
    '''Captures from a camera using ffmpeg

    (Only tested on so far!)

    Args:
        device: The device to use (by default, 0)
        avformat: The format to use in ffmpeg (avfoundation by default)
        width (int): width of capture (default 1280)
        height (int): height of capture (default 720)
    '''

    def __init__(self, device=0, avformat='avfoundation', pixel_format='yuyv422', width=1280, height=720, fps=30, **kwargs):
        params = '{}:{}?framerate={}&video_size={}x{}&pixel_format={}'.format(avformat, device, fps, width, height, pixel_format)
        Clip.__init__(self, params, **kwargs)

