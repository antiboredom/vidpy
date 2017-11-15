from vidpy import Composition, Clip

vid = 'videos/hand3.mp4'

filters = {
    'brightness': [.8],
    'contrast': [.9],
    'opacity': [.1],
    'hue': [.8],
    'saturate': [.9],
    'grayscale': [],
    'threshold': [],
    'dynamic_threshold': [],
    'invert': [],
    'extract_color': [],
    'glow': [],
    'softglow': [],
    'cartoon': [0.9],
    'chroma': [],
    'vflip': [],
    'hflip': [],
    'position': [100, 100, '30%', '30%'],
    'move': [[(0, '-100%', '-100%', '100%', '100%'), (30, 0, 0, '100%', '100%')]],
    'charcoal': [],
    'dust': [],
    'grain': [],
    'vignette': [],
    'mirror': [],
    'squareblur': [.01],
    'sharpness': [1],
    'luminance': [],
    'posterize': [],
    'pixelize': [],
    'gradient': [],
}

clips = []
for f in filters:
    clip = Clip(vid, start=0, end=1)
    clip.volume(0)

    args = filters[f]

    if len(args) > 0:
        getattr(clip, f)(*args)
    else:
        getattr(clip, f)()

    clip.text(f, olcolor='#000000', outline=10)
    clips.append(clip)

Composition(clips, singletrack=True).preview()
