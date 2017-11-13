from vidpy import Composition, Camera

clip = Camera(width=1280, height=720, start=0, end=5)
clip.spin(2)
Composition([clip]).save('camera.mp4')
