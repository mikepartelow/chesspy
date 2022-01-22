"""Implements an Enum representing Castle direction."""
from enum import Enum


class Castle(Enum):
    """Enum representing chess castling direction."""
    KINGSIDE = 1
    QUEENSIDE = 2
