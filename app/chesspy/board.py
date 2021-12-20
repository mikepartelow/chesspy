class Board:
    def __init__(self, reprstr=None):
        if reprstr is not None:
            self.squares = [ ' ' if ch is None else ch for ch in reprstr ]
        else:
            self.squares = [ 'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r',
                             'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 
                              None, None, None, None, None, None, None, None,
                              None, None, None, None, None, None, None, None,
                              None, None, None, None, None, None, None, None,
                              None, None, None, None, None, None, None, None,
                              'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 
                              'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R',
                            ]

    def __str__(self):
        s = []

        s.extend(['   0 ', ' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', '\n'])
        for y in range(0, 8):    
            s.append(f"{y} ")        
            for x in range(0, 8):                                
                square = self.squares[8*y + x]
                s.append(f"[{square or ' '}]")
            s.append(f" {8-y}\n")                        
        s.extend(['   a ', ' b ', ' c ', ' d ', ' e ', ' f ', ' g ', ' h '])

        return ''.join(s)

    def __repr__(self):
        return ''.join(ch or ' ' for ch in self.squares)

    def square_at(self, y, x):
        """Returns the Piece at the given coordinates, or None.

        Raises IndexError if coordinates are out of bounds.
        """

        if y < 0 or y > 7 or x < 0 or x > 7:
            raise IndexError

        return self.squares[8*y + x]

    def place_piece_at(self, piece, y, x):
        """Place the given piece on the board at the given coordinates.

        >>> b = Board()
        >>> b.place_piece_at('K', 2, 3)
        >>> b.squares[2*8+3]
        'K'

        Raises ArgumentError if coordinates are out of bounds.
        >>> Board().place_piece_at(None, -1, 8)
        Traceback (most recent call last):
        ...
        IndexError

        """
        if y < 0 or y > 7 or x < 0 or x > 7:
            raise IndexError

        self.squares[8*y+x] = piece