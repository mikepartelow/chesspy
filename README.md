# A FGDD Chess Platform in Python 3.10

> How do you test a chess engine? Famous Game Driven Development!

## Chess Engines

A chess engine examines chess board positions and suggests good moves. I decided to build a chess engine
because programming is fun, chess is fun, and I want to work with newer Python features and standard libraries.

There exist better chess engines than this, but I didn't have the pleasure of writing those from scratch.

### Build chesspy

    docker build -t chesspy .

### Run chesspy

    docker run -v `pwd`/app:/chesspy -ti chesspy bash
    python main.py board # display a chess board with pieces
    python main.py       # display a playthrough of The Immortal Game

### Test chesspy

    python -m unittest tests
    python -m unittest tests.test_san
    python -m unittest tests.test_san.TestMove
    python -m unittest tests.test_san.TestMove.test_0

### Split PGN test files

    pushd tests/games
    cat long.pgn | ./split_pgn 1500 long
    popd
    TEST_LONG=long python3.10 -m unittest tests

> On Mac, running tests with Docker bind mounts [slows the tests](https://github.com/docker/for-mac/issues/3677) down by about 15x.
> It's actually faster to rebuild the container and run the tests than to use bind mounts on a long-running container.

    docker build -qt chesspy . && docker run -t chesspy bash -c 'python -m unittest tests'


## One way to write a software Chess Engine

Although the definition of a Chess Engine is "software that generates good chess moves", it's useful
for any Chess Engine to also understand some chess move notation. Then we can build a fully featured
game for human vs. computer, and we can use historical games as training material for our engine.

Standard Algebraic Notation (SAN) is a widely used, standardized chess move notation. It is used by all
major chess organizations and websites, and understood by chess players of all nationalities. Games recorded
in SAN are easily obtainable on the internet or in centuries-old chess manuals at your public library.

SAN is relatively simple for humans to understand. But what seems simple to a human can require pretty
complicated code to implement in software.

Consider the following board position, with Black's Queen on e4, and White's Knights on c3 and e3.

```
      [r][n][b][ ][k][b][n][r] 8
      [p][p][p][p][p][p][p][p] 7
      [ ][ ][ ][ ][ ][ ][ ][ ] 6
      [ ][ ][ ][ ][ ][ ][ ][ ] 5
      [ ][ ][ ][ ][q][ ][ ][ ] 4
      [ ][ ][N][ ][N][ ][ ][ ] 3
      [P][P][P][P][ ][P][P][P] 2
      [R][ ][B][Q][K][B][ ][R] 1
       a  b  c  d  e  f  g  h
```

What does the SAN move "Nd5" mean? It means "Knight to d5". Both of white's knights can reach d5 in one move,
but if you are familiar with the rules of chess, it is clear that only the knight on c3 can legally move.

The rules of chess state that a piece cannot be moved if moving it would expose the King to check. If
White moves her e3 Knight, Black's Queen gives check. Therefore, the move "Nd5" unambiguously means to
move the Knight from c3, not the one from e3.

For a Chess Engine to reliably parse a simple looking SAN move like "Nd5", it must know all the rules of chess, and it must
also know the state of the current game. Given "Nd5", a Chess Engine can't necessarily
figure out exactly which piece to move just by processing the text of a three character string.

This is not simply a matter of forbidding illegal moves. Many SAN strings (like "Nd5") specify only
the kind of piece to move and the destination square.

Consider this board position.

```
      [r][n][b][q][k][b][n][r] 8
      [p][p][p][p][p][p][p][p] 7
      [ ][ ][ ][ ][ ][ ][ ][ ] 6
      [ ][ ][ ][ ][ ][ ][ ][ ] 5
      [ ][ ][ ][ ][ ][ ][ ][ ] 4
      [ ][ ][N][ ][ ][ ][ ][ ] 3
      [P][P][P][P][P][P][P][P] 2
      [R][ ][B][Q][K][B][N][R] 1
       a  b  c  d  e  f  g  h
```

If Black moves "Nf6", the Chess Engine needs more information than is provided in the 3 character string
to conclude the Knight to move is currently on g8. It has to know the current board state and how Knights move,
among other details.

## The Testing Problem

I like Test Driven Development (TDD), where we write our tests and then we write just enough code to make our tests pass.

How do I know my tests are good? I can write some simple bootstrapping tests validating basic moves. But to
engineer real confidence in my SAN parser, I'll need lots more test cases than I am willing to manually
type out.

Fortunately, there are plenty of fully validated chess games represented in SAN format all over the internet.

Many of them are Famous. That's where Famous Game Driven Development comes in!


### Famous Game Driven Development (FGDD)

The idea is simple: leverage the existing universe of chess games that have already been validated correct
by human referees or existing chess engines. Those games are made of legal moves, so my Chess Engine should
have no problem parsing and executing those moves.

#### FGDD Heavy

I started with two Famous Chess Games: The Immortal Game and The Game of the Century.

We already know all the moves in these games are legal (and some are brilliant), so if my Engine can't
make the correct move when given the legal SAN move strings from these games, I know immediately my code
is wrong.

I populated a simple text file with the SAN formatted moves from these games.

I fed the moves to my SAN parser. For each move, I wrote the code to execute the move, and printed out
a 64 (8x8) character text representation of the board state, and a visual representation of the board state.

I manually (visually!) verified that my engine made the right move, and then added the 64 character
text representation of the board state to a "known good" file.

The next time I ran my tests, the tests compared manually verified "known good" board states to what the
engine did with each move. This way I could catch any bugs that I introduced after verifying prior
move implementations.

[FGDD Heavy](app/tests/test_game.py#L117)

Once the engine could play through all the moves I had some confidence that my engine could parse some
subset of SAN, and I had a suite of tests to detect regression bugs as I continued.

#### FGDD Light

With the "Heavy" FGDD tests as a foundation, I was ready to feed the engine more "known good" chess games
that were already validated by some other chess engine. I downloaded PGN formatted files of my own lichess
games and some PGN files for other lichess users.

Parsing the PGN files and running the moves through the engine would not directly test the correctness
of the engine, but it could flush out unimplemented cases and bugs. For example, The Immortal Game and
The Game Of The Century contain neither "pawn promotion" nor "en passant".

In both cases the engine did not catch any error directly, but a few moves after the engine made a mistake,
it could not execute a move it normally could have handled.

For example, when executing pawn promotion like "h8=Q", the engine simply ignored the promotion to Queen
and moved the pawn to h8. A few moves later, the player moved their Queen, but my engine could find no
Queen on the board! So it raised an exception, I looked at the move history, and added tests specifically
for Pawn Promotion.

With a large dataset of less-famous games, I can flush out many cases that I would miss if I tried to imagine
individual test tests myself.

[FGDD Light](app/tests/test_pgn.py#L34)

#### FGDD for Move Suggestions

Eventually my Chess Engine will do what Chess Engines are supposed to do - suggest moves given specific
game states (board positions).

I can use FGDD for partially testing that functionality, as well. For example, I can take existing games
in PGN format and ensure that for each move in the already validated game, my Engine suggests at least
the move that was actually played.

That won't tell me whether the other suggestions are legal, or whether any of the suggestions are good
moves, but it does serve as a solid testing foundation.

#### Finalizing the Tests

FGDD is a fun solution to a challenging testing problem. But it will not provide full confidence in the
correctness of my code. More work is required for that!

