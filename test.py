'''Unit Test file'''
import unittest


class TestToto(unittest.TestCase):

    def test_toto(self):
        print('toto')

    def test_totoe(self):
        print('toto')

    @classmethod
    def setUpClass(cls):
        print('Setup Class')

    @classmethod
    def tearDownClass(cls):
        print('TaerDown Class')

if __name__ == '__main__':
    unittest.main()
