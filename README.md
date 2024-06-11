
# Flip Chess

Flip Chess is a simplified version of chess with only 32 squares and simplified movement and capturing rules. This project includes the implementation of the game, a graphical user interface using Pygame, and AI agents using Q-Learning and MinMax algorithms to play the game.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [AI Agents](#ai-agents)
- [Project Structure](#project-structure)
- [Author](#author)

## Installation

To run this project, you need to have Python installed. Additionally, install the required packages by running:

```bash
pip install pygame numpy
```



## Usage

To play the game against the AI:

```bash
python main.py
```

To train the AI agents with visual display:(train small amount of times with visual delay)

```bash
python train_ai_with_display.py
```

To train the AI agents without visual display (train large amount of times):

```bash
python train_ai_without_display.py
```
If you want to play against the Q-Learning AI, please train the AI first by running one of the train scripts mentioned above.

## Game Rules

1. The game is played on a 4x8 grid.
2. Each player starts with a set of pieces including Kings, Queens, Rooks, Bishops, Knights, and Pawns.
3. Pieces can only move one square at a time either horizontally or vertically.
4. Pieces can capture other pieces according to specific rules:
   - Kings can capture anything except Pawns.
   - Queens can capture anything except Kings.
   - Rooks can capture anything except Kings and Queens.
   - Bishops can capture anything except Kings, Queens, and Rooks.
   - Knights can capture anything except Kings, Queens, Rooks, and Bishops.
   - Pawns can only capture Kings and other Pawns.
5. The goal is to capture all opponent pieces or prevent the opponent from making any valid moves.

## AI Agents

### Q-Learning Agent

The Q-Learning agent uses a Q-table to learn the best actions based on the state of the board. It updates the Q-table using the Q-learning update rule.


### MinMax Agent

The MinMax agent uses the MinMax algorithm with a specified depth to evaluate the best possible move by considering all possible moves and their outcomes.

## Author

Henry Shi
