import unittest
import os
from vidpy import utils

class TestUtils(unittest.TestCase):
    def test_timestamp(self):
        ts = utils.timestamp(None)
        self.assertEqual(ts, None)

        ts = utils.timestamp(10)
        self.assertIsInstance(ts, utils.Second)


    def test_second(self):
        s = utils.Second

        self.assertEqual(s(0), 0.0)
        self.assertEqual(str(s(0)), ':0.000000')

        self.assertEqual(s(1) + s(2), 3)
        self.assertEqual(s(1) + 2, 3)

        self.assertEqual(s(3) - s(2), 1)
        self.assertEqual(s(3) - 2, 1)

        self.assertEqual(s(3) * s(2), 6)
        self.assertEqual(s(3) * 2, 6)

        self.assertEqual(s(1) / s(2), 0.5)
        self.assertEqual(s(1) / 2, 0.5)


    @unittest.skipIf('TRAVIS' in os.environ and os.environ['TRAVIS'] == 'true', 'Skipping this test on Travis')
    def test_get_melt_profie(self):
        profile = utils.get_melt_profile(os.path.realpath('demos/videos/hand1.mp4'))
        self.assertEqual(profile['total_frames'], 251)
        self.assertEqual(profile['width'], 1280)
        self.assertEqual(profile['height'], 720)
        self.assertAlmostEqual(profile['duration'], 4.18000)
        self.assertEqual(profile['fps'], 60)
