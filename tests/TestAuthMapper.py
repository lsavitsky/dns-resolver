import unittest
import sys 
import logging
# from unittest.mock import patch
# import io

sys.path.append('../')
import AuthMapper

class TestAuthMapper(unittest.TestCase):

    def SetUp(self):
        self.mapper1 = AuthMapper.AuthMapper()

    def TestFirst(self):
        actual = self.mapper1(1).map
        logging.basicConfig(level = logging.INFO)
        logging.info(actual)
        
        
mapper1 = AuthMapper.AuthMapper()       
# actual = mapper1(1).map
# print(actual)
if __name__ == '__main__':
    unittest.main()