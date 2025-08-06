import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tracking.backends import DummyBackend

class TestBackends(unittest.TestCase):

    def test_dummy_backend(self):
        backend = DummyBackend()
        self.assertIsNotNone(backend)
        backend.connect(None)
        backend.updatepose(None, None, None, None)
        backend.disconnect()

if __name__ == '__main__':
    unittest.main()
