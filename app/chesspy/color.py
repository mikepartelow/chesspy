"""Implements an Enum representing piece color."""
from enum import Enum


class Color(Enum):
    """Enum representing chess piece colors."""
    WHITE = 1
    BLACK = 2

    def __str__(self):
        return "white" if self == Color.WHITE else "black"

    def opponent(self):
        """Returns Black if the color of self is White, returns White if the color of self is Black."""
        return self.BLACK if self == self.WHITE else self.WHITE

    @staticmethod
    def toggle(color):
        """Returns Black if the given color is White, returns White if the given color is Black."""
        return Color.BLACK if color == Color.WHITE else Color.WHITE


def color_of(ch):
    """Returns Color.WHITE if given piece character is White, otherwise Color.BLACK.

    Performs no validation."""
    if ch.isupper():
        return Color.WHITE
    return Color.BLACK


def colorize(ch, color):
    """Returns the given piece, ch, altered to represent the given color.

    Performs no validation."""
    if color == Color.WHITE:
        return ch.upper()
    return ch.lower()


def opponent(ch):
    """Returns the opponent's piece of the same kind. Given White King returns Black King, etc."""
    if ch.isupper():
        return ch.lower()
    return ch.upper()
