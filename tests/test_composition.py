import os
import unittest
from xml.etree.ElementTree import fromstring
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


    def test_autoset_duration(self):
        xmlstring = '''<melt>
            <tractor out="100" />
            <profile width="1280" height="720" display_aspect_num="1280" display_aspect_den="720" frame_rate_num="30" />
            <producer><property name="length" /></producer>
            <playlist><entry /></playlist>
        </melt>'''

        comp = Composition([])
        xml = comp.autoset_duration(fromstring(xmlstring))
        self.assertEqual(xml.find('tractor').get('out'), '100')
        self.assertEqual(xml.find('producer').get('out'), '100')
        self.assertEqual(xml.find('./playlist/entry').get('out'), '100')

        comp = Composition([], duration=2.5)
        xml = comp.autoset_duration(fromstring(xmlstring))
        self.assertEqual(xml.find('tractor').get('out'), ':2.500000')
        self.assertEqual(xml.find('producer').get('out'), ':2.500000')
        self.assertEqual(xml.find('./playlist/entry').get('out'), ':2.500000')


    def test_set_meta(self):
        xmlstring = '''<melt>
            <tractor out="100" />
            <profile width="1280" height="720" display_aspect_num="1280" display_aspect_den="720" frame_rate_num="30" />
            <producer><property name="length" /></producer>
            <playlist><entry /></playlist>
        </melt>'''

        comp = Composition([], width=100, height=200, fps=60)
        xml = comp.set_meta(fromstring(xmlstring))
        profile = xml.find('profile')
        self.assertEqual(profile.get('width'), '100')
        self.assertEqual(profile.get('height'), '200')
        self.assertEqual(profile.get('frame_rate_num'), '60')


    @unittest.skipIf('TRAVIS' in os.environ and os.environ['TRAVIS'] == 'true', 'Skipping this test on Travis')
    def test_xml(self):
        clip = Clip('demos/videos/hand1.mp4')
        clip2 = Clip('demos/videos/hand2.mp4')

        # by default, the duration/width/height/fps should be set automatically
        comp = Composition([clip, clip2])
        xml = fromstring(comp.xml())
        profile = xml.find('profile')
        self.assertEqual(profile.get('width'), '1280')
        self.assertEqual(profile.get('height'), '720')
        self.assertEqual(profile.get('frame_rate_num'), '60')
        self.assertEqual(xml.find('tractor').get('out'), '250')
        self.assertEqual(xml.find('producer').get('out'), '250')
        self.assertEqual(xml.find('./playlist/entry').get('out'), '250')

        # overwrite fps, width, height, duration
        comp = Composition([clip, clip2], duration=10, width=100, height=50, fps=30)
        xml = fromstring(comp.xml())
        profile = xml.find('profile')
        self.assertEqual(profile.get('width'), '100')
        self.assertEqual(profile.get('height'), '50')
        self.assertEqual(profile.get('frame_rate_num'), '30')
        self.assertEqual(xml.find('tractor').get('out'), ':10.000000')
        self.assertEqual(xml.find('producer').get('out'), ':10.000000')
        self.assertEqual(xml.find('./playlist/entry').get('out'), ':10.000000')

        # test duration for singletrack
        comp = Composition([clip, clip2], singletrack=True)
        xml = fromstring(comp.xml())
        self.assertEqual(xml.find('tractor').get('out'), '396')
        self.assertEqual(xml.find('producer').get('out'), '396')
        self.assertEqual(xml.find('./playlist/entry').get('out'), '396')


if __name__ == '__main__':
    unittest.main()
