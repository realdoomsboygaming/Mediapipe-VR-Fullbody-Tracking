import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.helpers import mediapipeTo3dpose, get_rot, get_rot_mediapipe

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.pose3d = np.random.rand(29, 3)

    def test_mediapipeTo3dpose(self):
        class Landmark:
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z

        class LandmarkList:
            def __init__(self):
                self.landmark = [Landmark(i, i*2, i*3) for i in range(33)]

        lms = LandmarkList()
        pose = mediapipeTo3dpose(lms.landmark)
        self.assertEqual(pose.shape, (29, 3))
        self.assertTrue(np.all(pose[0] == [28, 56, 84]))
        self.assertTrue(np.all(pose[7] == [11.5, 23, 34.5]))

    def test_get_rot(self):
        rot_hip, rot_leg_l, rot_leg_r = get_rot(self.pose3d)
        self.assertEqual(len(rot_hip), 4)
        self.assertEqual(len(rot_leg_l), 4)
        self.assertEqual(len(rot_leg_r), 4)
        
    def test_get_rot_mediapipe(self):
        hip_rot, l_foot_rot, r_foot_rot = get_rot_mediapipe(self.pose3d)
        self.assertEqual(len(hip_rot), 4)
        self.assertEqual(len(l_foot_rot), 4)
        self.assertEqual(len(r_foot_rot), 4)

if __name__ == '__main__':
    unittest.main()
