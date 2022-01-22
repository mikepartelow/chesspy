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
