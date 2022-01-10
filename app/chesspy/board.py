import logging
import itertools

class Board:
    def __init__(self, reprstr=None):
        if reprstr is not None:
            assert(len(reprstr) == 8*8)
            self.squares = [ None if ch == ' ' else ch for ch in reprstr ]
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

    def find_first(self, squares, src_y=None, src_x=None):
        """Find the first piece encountered in the list of squares. 

        If src_y or src_x are not None, return only coords that include them.

        Returns (piece, y, x) or None.
        """
        logging.debug("find_first(%r, %r, %r)", squares, src_y, src_x)

        for y, x in squares:
            logging.debug("(%s, %s)", y, x)
            if y < 0 or y > 7 or x < 0 or x > 7:
                # FIXME: this should never happen if we computed things correctly above.
                raise IndexError

            if (p := self.squares[8*y + x]) is not None:
                if src_y in (None, y) and src_x in (None, x):
                    return (p, y, x)

    def find_first_on_h_or_v(self, start, inc_y, inc_x, src_y=None, src_x=None):
        """Find the first piece encountered horizontally or vertically starting from (start_y, start_x) while incrementing (y, x) by (inc_y, inc_x)

        Either inc_y or inc_x must == 0.
        If src_y or src_x are not None, return only coords that include them.

        Returns tuple (p, y, x) where p is the first piece encountered, (y, x) are coordinates of p, or None if no piece is found.
        """
        start_y, start_x = start
        logging.debug("find_first_on_h_or_v(%s, %s, %s, %s, %s, %s)", start_y, start_x, inc_y, inc_x, src_y, src_x)

        assert((inc_y == 0 or inc_x == 0) and (inc_y != 0 or inc_x != 0))

        if inc_y != 0:
            dst_y = -1 if inc_y < 0 else 8
            logging.debug(" dst_y=%d, start_y+inc_y=%d, dst_y=%d, inc_y=%d", dst_y, start_y+inc_y, dst_y, inc_y)
            y_range = range(start_y+inc_y, dst_y, inc_y)
        else:
            y_range = [start_y]

        if inc_x != 0:
            dst_x = -1 if inc_x < 0 else 8
            logging.debug(" dst_x=%d, start_x+inc_x=%d, dst_x=%d, inc_x=%d", dst_x, start_x+inc_x, dst_x, inc_x)
            x_range = range(start_x+inc_x, dst_x, inc_x)
        else:
            x_range = [start_x]

        return self.find_first(list(itertools.product(y_range, x_range)), src_y, src_x)

    def find_first_on_diagonal(self, start, inc_y, inc_x, src_y=None, src_x=None):
        """Find the first piece encountered diagonally starting from (start_y, start_x) while incrementing (y, x) by (inc_y, inc_x)

        If src_y or src_x are not None, return only coords that include them.

        Returns tuple (p, y, x) where p is the first piece encountered, (y, x) are coordinates of p, or None if no piece is found.
        """
        start_y, start_x = start
        logging.debug("find_first_on_diagonal(%s, %s, %s, %s, %s, %s)", start_y, start_x, inc_y, inc_x, src_y, src_x)

        assert(inc_y in [-1, 1] and inc_x in [-1, 1])        

        dst_y = -1 if inc_y < 0 else 8
        logging.debug(" dst_y=%d, start_y+inc_y=%d, dst_y=%d, inc_y=%d", dst_y, start_y+inc_y, dst_y, inc_y)
        y_range = range(start_y+inc_y, dst_y, inc_y)

        dst_x = -1 if inc_x < 0 else 8
        logging.debug(" dst_x=%d, start_x+inc_x=%d, dst_x=%d, inc_x=%d", dst_x, start_x+inc_x, dst_x, inc_x)
        x_range = range(start_x+inc_x, dst_x, inc_x)

        return self.find_first(list(zip(y_range, x_range)), src_y, src_x)
