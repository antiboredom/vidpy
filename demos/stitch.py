from vidpy import Clip, Composition

clip1 = Clip('videos/hand1.mp4')
clip2 = Clip('videos/hand2.mp4')
clip3 = Clip('videos/hand3.mp4')

clips = [clip1, clip2, clip3]


# stitch all clips together
stiched = Composition(clips, singletrack=True)
stiched.save('allvids.mp4')

# stitch the first second of all clips
for clip in clips:
    clip.cut(start=0, end=1)

stiched = Composition(clips, singletrack=True)
stiched.save('firstsecond.mp4')
