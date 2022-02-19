import os
import logging

TEST_LOG_PATH = 'logs/chesspy.test.log'
if os.path.exists(TEST_LOG_PATH):
    os.unlink(TEST_LOG_PATH)

logging.basicConfig(filename=TEST_LOG_PATH,
    encoding='utf-8',
    format='[%(levelname).1s]::[%(filename)s:%(lineno)d]::[%(message)s]',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

from .test_san import *
from .test_pgn import *
from .test_game import *
from .test_color import *
from .test_board import *
from .test_players import *
from .test_analyzers import *
from .test_move_generators import *