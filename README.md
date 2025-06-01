# IQVIPER — Snake Game with Prolog AI

A Snake game implementation with an AI agent powered by Prolog for intelligent decision making. This hybrid system demonstrates how symbolic reasoning (via SWI-Prolog) can be used to navigate the classic Snake game through Python.

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install SWI-Prolog from:  
https://www.swi-prolog.org/download/stable

3. Run the game:
```bash
python game/snake.py
```

## Project Structure

```
snakemind/
├── game/
│   └── snake.py               # Main Snake game using Pygame
├── agent/
│   └── controller.py          # Controls decision-making from Prolog
├── prolog/
│   └── snake_knowledge.pl     # Prolog knowledge base and logic rules
├── utils/
│   └── prolog_bridge.py       # Python-SWI Prolog bridge using pyswip
├── assets/                    # (Optional) Images, sounds
├── requirements.txt
└── README.md
```

## How It Works

- The game sends the current state (head position, food, snake body) to Prolog.
- Prolog evaluates possible directions and determines safe or optimal moves using logic rules.
- Python reads the result from Prolog and moves the snake accordingly.
- This setup showcases symbolic AI instead of traditional machine learning.

## Example Prolog Logic

```prolog
safe_direction(up) :- not(unsafe(up)).
unsafe(up) :- head_position(_, Y), Y =< 0.
```

## Requirements

- Python 3.x
- SWI-Prolog
- Python packages:
  - pygame
  - pyswip

`requirements.txt` should include:
```
pygame
pyswip
```

## Author

Developed by [Muhammad_Abu-Bakr]  
Project Name: IQViper  
An experiment in integrating symbolic AI into classic gameplay.
