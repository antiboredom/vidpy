from vidpy import Clip, Composition

clip = Clip('videos/hand2.mp4')
clip.speed(0.1)
clip.preview()
# Composition([clip]).preview()
