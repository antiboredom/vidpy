from vidpy import Clip, Composition

background_clip = Clip('videos/hand1.mp4')
clip = Clip('videos/hand2.mp4')

# create a clip to use a as a mask
# you can use use a video,text clip or an image
mask = Clip('videos/mask.png')

# you can also add effects to the mask
mask.glow('0=0;200=.9')

# make sure that the duration of the mask is the same as the clip
# (or don't, if you only want the mask to affect part of the clip)
mask.set_duration(clip.duration)

# set the mask on the clip
clip.set_mask(mask)

comp = Composition([background_clip, clip])
comp.preview()

