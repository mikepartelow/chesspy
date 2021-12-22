import os
import logging

TEST_LOG_PATH = 'logs/chesspy.test.log'
os.unlink(TEST_LOG_PATH)
logging.basicConfig(filename=TEST_LOG_PATH, encoding='utf-8', level=logging.DEBUG)

from .test_san import *
from .test_board import *
from .test_game import *