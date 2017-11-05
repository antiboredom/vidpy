from vidpy import Clip, Composition

video = 'videos/hand1.mp4'

canvas_width = 1280
canvas_height = 720
vid_width = canvas_width/3
vid_height = (vid_width/canvas_width) * canvas_height

x = 0
y = 0

clips = []

while y < canvas_height:
    # create a clip
    clip = Clip(video)

    # set clip position
    clip.position(x=x, y=y, w=vid_width, h=vid_height)

    # fade in for 1/2 second
    clip.fadein(0.5)

    # repeat the clip three times
    clip.repeat(3)

    # start the clip based on existing clips
    clip.set_offset(len(clips)*.1)

    clips.append(clip)

    # increment the x and y position
    x += vid_width
    if x > canvas_width:
        y += vid_height
        x = 0

grid = Composition(clips, width=canvas_width, height=canvas_height)
grid.save('grid.mp4')
