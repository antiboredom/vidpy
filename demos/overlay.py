import glob
from vidpy import Composition, Clip

clips = [Clip(v) for v in glob.glob('./videos/*.mp4')]
clips = [c.opacity(.5) for c in clips]

Composition(clips).preview()
