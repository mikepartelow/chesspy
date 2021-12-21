from enum import Enum

class Color(Enum):
	WHITE = 1
	BLACK = 2

	def __str__(self):
		return "white" if self == Color.WHITE else "black"

	@staticmethod
	def toggle(color):
		return Color.BLACK if color == Color.WHITE else Color.WHITE
