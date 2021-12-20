# A FGDD Chess Platform in Python 3.10

> It's time to brush up on my Python Best Practices. What better way than to develop a chess program?

## Focuses

- TDD
- FGDD: Famous Game Driven Development. Use games like Game Of The Century and The Immortal Game for TDD.
- Prefer stdlib over rolling my own
- Prefer rolling my own over 3rd party libs - point is to learn and explore

## Build

    docker build -t chesspy .

## Run

    docker run -ti -v `PWD`/app:/chesspy -ti chesspy bash
    python main.py board
    python main.py

## Test
    
    python -m unittest tests
    python -m unittest tests.test_san
    python -m unittest tests.test_san.TestMove
    python -m unittest tests.test_san.TestMove.test_0
    

## Ideas, FIXMEs, TODOs
    - [ ] way to run all doctests for all files
    - [ ] git pre-commit that demands no FIXMEs
    - [ ] git pre-commit that requires docstrings
    - [ ] Deluxe logging
    - [ ] san.parse(sanstr, game). when passing game, we can fully populate Move().
    - [ ] coverage stats for unit tests
    - [ ] exception heirarchy - not IndexError for everything
    - [ ] basic integration test that uses gotc and immortal
    - [ ] TDD game_test FAN
    - [ ] TDD PGN
    - [ ] download some GM's lichess PGN and turn it into an integration test
    - [ ] networked 2 player
    - [ ] an AI mode that can beat me
    - [ ] an AI mode that can beat Magnus
