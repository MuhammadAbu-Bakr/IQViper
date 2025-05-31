# Snake Game with Prolog AI

A Snake game implementation with an AI agent powered by Prolog for intelligent decision making.

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install SWI-Prolog from https://www.swi-prolog.org/download/stable

3. Run the game:
```bash
python game/snake.py
```

## Project Structure

- `game/snake.py`: Main Snake game implementation using Pygame
- `prolog/snake_knowledge.pl`: Prolog knowledge base and reasoning rules
- `agent/controller.py`: Interface between Prolog and game logic
- `utils/prolog_bridge.py`: Python-Prolog bridge implementation
- `assets/`: Game resources (sprites, sounds)
