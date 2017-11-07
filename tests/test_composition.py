import unittest
from vidpy import Composition, config, Clip

class TestComposition(unittest.TestCase):
    '''
    TODO:
        preview()
        xml()
        save()
        save_xml()
        duration tests
        width/height/fps tests
    '''

    def test_empty_composition(self):
        config.MELT_BINARY = 'melt'
        comp = Composition([])
        self.assertEqual(str(comp), 'melt -track color:#000000 out=0')


    def test_basic_singletrack_composition(self):
        config.MELT_BINARY = 'melt'
        clip = Clip('video.mp4')
        clip2 = Clip('video2.mp4')
        comp = Composition([clip, clip2], singletrack=True)
        self.assertEqual(str(comp), 'melt -track color:#000000 out=0 -track video.mp4 in=":0.000000" video2.mp4 in=":0.000000" -transition composite distort=1 a_track=0 b_track=1')


    def test_basic_multitrack_composition(self):
        config.MELT_BINARY = 'melt'
        clip = Clip('video.mp4')
        comp = Composition([clip])
        self.assertEqual(str(comp), 'melt -track color:#000000 out=0 -track video.mp4 in=":0.000000" -transition composite distort=1 a_track=0 b_track=1 -transition mix a_track=0 b_track=1')


    def test_multitrack_composition(self):
        config.MELT_BINARY = 'melt'
        clip = Clip('video.mp4')
        clip2 = Clip('video2.mp4')
        comp = Composition([clip, clip2])
        self.assertEqual(str(comp), 'melt -track color:#000000 out=0 -track video.mp4 in=":0.000000" -track video2.mp4 in=":0.000000" -transition composite distort=1 a_track=0 b_track=1 -transition mix a_track=0 b_track=1 -transition composite distort=1 a_track=0 b_track=2 -transition mix a_track=0 b_track=2')




if __name__ == '__main__':
    unittest.main()
