import glob
from vidpy import Composition, Clip

clips = [Clip(v) for v in glob.glob('/Users/sam/Downloads/test*.mov')]
clips = [c.opacity(.5) for c in clips]

Composition(clips).preview()
