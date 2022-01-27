"""Implements a class representing chess moves."""

import logging
import collections
from .board import Pos

# pylint: disable=too-many-instance-attributes
class Move:
    """Represents a chess move, including piece to move, source coordinates, destination coordinates, etc."""
    src_y = None
    src_x = None
    dst_y = None
    dst_x = None
    piece = None
    promotion = None
    check = False
    mate = False
    capture = False
    castle = False
    en_passant = False

    def __setattr__(self, name, value):
        """Forbid setting attributes twice, unless to same value after initialization."""
        if name in ['check', 'mate', 'capture', 'castle', 'en_passant']:
            if getattr(self, name) is not False:
                raise IndexError
            return super().__setattr__(name, value)

        if getattr(self, name) not in (None, value):
            if getattr(self, name):
                logging.debug("%s != %s", getattr(self, name), value)
            raise IndexError

        return super().__setattr__(name, value)

    def __repr__(self):
        return("Move({"
               f"src_y: {self.src_y}, "
               f"src_x: {self.src_x}, "
               f"dst_y: {self.dst_y}, "
               f"dst_x: {self.dst_x}, "
               f"piece: {self.piece}, "
               f"promotion: {self.promotion}, "
               f"check: {self.check}, "
               f"mate: {self.mate}, "
               f"capture: {self.capture}, "
               f"castle: {self.castle}, "
               "})")

    @property
    def dst(self):
        """Returns Pos(y, x) coordinates for move destination."""
        return Pos(self.dst_y, self.dst_x)

    @property
    def src(self):
        """Returns Pos(y, x) coordinates for move source."""
        return Pos(self.src_y, self.src_x)
