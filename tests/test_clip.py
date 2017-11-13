import os
import unittest
from xml.etree.ElementTree import fromstring
from vidpy import Composition, config, Clip

class TestClip(unittest.TestCase):
    def test_args(self):
        clip = Clip('video.mp4')
        self.assertEqual(str(clip), '-track video.mp4 in=":0.000000"')

        clip = Clip('video.mp4', start=1.5)
        self.assertEqual(str(clip), '-track video.mp4 in=":1.500000"')

        clip = Clip('video.mp4', start=1.1, end=3)
        self.assertEqual(str(clip), '-track video.mp4 in=":1.100000" out=":3.000000"')

        clip = Clip('video.mp4', offset=2)
        self.assertEqual(str(clip), '-track -blank :2.000000 video.mp4 in=":0.000000"')

        clip = str(Clip('video.mp4', somearg=5, anotherarg="hi"))
        self.assertTrue(' somearg="5"' in clip)
        self.assertTrue(' anotherarg="hi"' in clip)


    def test_cut(self):
        clip = Clip('video.mp4').cut(start=1.1, end=3)
        self.assertEqual(str(clip), '-track video.mp4 in=":1.100000" out=":3.000000"')

        clip = Clip('video.mp4').cut(start=1.1)
        self.assertEqual(str(clip), '-track video.mp4 in=":1.100000"')

        clip = Clip('video.mp4').cut(end=2)
        self.assertEqual(str(clip), '-track video.mp4 in=":0.000000" out=":2.000000"')

        clip = Clip('video.mp4').cut(start=1, duration=3)
        self.assertEqual(str(clip), '-track video.mp4 in=":1.000000" out=":4.000000"')


    def test_set_duration(self):
        clip = Clip('video.mp4').set_duration(2)
        self.assertEqual(str(clip), '-track video.mp4 in=":0.000000" out=":2.000000"')


    def test_set_offset(self):
        clip = Clip('video.mp4').set_offset(2)
        self.assertEqual(str(clip), '-track -blank :2.000000 video.mp4 in=":0.000000"')


    def test_speed(self):
        clip = Clip('video.mp4').speed(.5)
        self.assertEqual(str(clip), '-track timewarp:0.5:video.mp4 in=":0.000000"')

        clip = Clip('video.mp4').speed(2)
        self.assertEqual(str(clip), '-track timewarp:2:video.mp4 in=":0.000000"')


    def test_repeat(self):
        clip = Clip('video.mp4').repeat(20)
        self.assertEqual(str(clip), '-track video.mp4 in=":0.000000" -repeat 20')


    def test_fx(self):
        clip = Clip('video.mp4').fx('somefx')
        self.assertEqual(str(clip), '-track video.mp4 in=":0.000000" -attach-track somefx')

        clip = Clip('video.mp4').fx('somefx')
        self.assertEqual(' '.join(clip.args(singletrack=True)), 'video.mp4 in=":0.000000" -attach-clip somefx')

        clip = str(Clip('video.mp4').fx('somefx', {'param1': 2, 'param2': 'hello'}))
        self.assertTrue('-track video.mp4 in=":0.000000" -attach-track somefx' in clip)
        self.assertTrue(' param1="2"' in clip)
        self.assertTrue(' param2="hello"' in clip)


    @unittest.skipIf('TRAVIS' in os.environ and os.environ['TRAVIS'] == 'true', 'Skipping this test on Travis')
    def test_profie(self):
        clip = Clip(os.path.realpath('demos/videos/hand1.mp4'))

        self.assertAlmostEqual(clip.original_duration, 4.18000)
        self.assertAlmostEqual(clip.duration, 4.18000)
        self.assertEqual(clip.total_frames, 251)
        self.assertEqual(clip.original_fps, 60)
        self.assertEqual(clip.width, 1280)
        self.assertEqual(clip.height, 720)


if __name__ == '__main__':
    unittest.main()

