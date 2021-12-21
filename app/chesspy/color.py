from enum import Enum

class Color(Enum):
	WHITE = 1
	BLACK = 2

	@staticmethod
	def toggle(color):
		return Color.BLACK if color == Color.WHITE else Color.WHITE
