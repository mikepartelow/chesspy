# A FGDD Chess Platform in Python 3.10

> It's time to brush up on my Python Best Practices. What better way than to develop a chess program?

Standard Algebraic Notation (SAN) is a widely used, standardized chess move notation. This version of **chesspy** parses SAN to replay games. **chesspy** 1.0 will feature two-player head-to-head and internet modes. Fun!

## Focuses

- TDD: Test Driven Development
- FGDD: Famous Game Driven Development. Use games like Game Of The Century and The Immortal Game to reveal necessary tests for TDD.
- Prefer stdlib over rolling my own.
- Prefer rolling my own over 3rd party libs - point is to learn and explore.

## Build

    docker build -t chesspy .

## Run

    docker run -ti -v `PWD`/app:/chesspy -ti chesspy bash
    python main.py board # display a chess board with pieces
    python main.py       # display a playthrough of The Immortal Game

## Test
    
    python -m unittest tests
    python -m unittest tests.test_san
    python -m unittest tests.test_san.TestMove
    python -m unittest tests.test_san.TestMove.test_0
    
