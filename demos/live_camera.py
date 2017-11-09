from vidpy import Composition, Clip

url = 'http://webcam.gordon.edu/mjpg/video.mjpg'
clip = Clip(url)
clip.spin(2)

clip.set_duration(10)
clip.save('live_spin.mp4')
