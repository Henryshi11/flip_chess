# train_ai_with_display.py
# Author: Henry Shi

import pygame
import sys
import time
from board import Board
from qlearning_agent import QLearningAgent

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 400
ROWS, COLS = 4, 8
SQUARE_SIZE = WIDTH // COLS

# Define colors
WHITE, BLACK, BLUE, RED, LIGHT_BLUE = (255, 255, 255), (0, 0, 0), (0, 0, 255), (255, 0, 0), (173, 216, 230)

# Create window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flip Chess')

# Load piece images (example)
PIECE_IMAGES = {
    'K_black': pygame.transform.scale(pygame.image.load('../images/king_black.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'K_white': pygame.transform.scale(pygame.image.load('../images/king_white.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'Q_black': pygame.transform.scale(pygame.image.load('../images/queen_black.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'Q_white': pygame.transform.scale(pygame.image.load('../images/queen_white.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'R_black': pygame.transform.scale(pygame.image.load('../images/rook_black.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'R_white': pygame.transform.scale(pygame.image.load('../images/rook_white.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'B_black': pygame.transform.scale(pygame.image.load('../images/bishop_black.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'B_white': pygame.transform.scale(pygame.image.load('../images/bishop_white.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'N_black': pygame.transform.scale(pygame.image.load('../images/knight_black.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'N_white': pygame.transform.scale(pygame.image.load('../images/knight_white.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'P_black': pygame.transform.scale(pygame.image.load('../images/pawn_black.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'P_white': pygame.transform.scale(pygame.image.load('../images/pawn_white.png'), (SQUARE_SIZE, SQUARE_SIZE)),
}

def draw_board(win, board):
    """
    Draw the game board.

    Parameters:
    win (pygame.Surface): The game window.
    board (Board): The game board.
    """
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BLUE if board.grid[row][col] is not None and not board.grid[row][col].revealed else (BLUE if (row + col) % 2 == 0 else RED)
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(win, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

def draw_pieces(win, board):
    """
    Draw the pieces on the board.

    Parameters:
    win (pygame.Surface): The game window.
    board (Board): The game board.
    """
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.grid[row][col]
            if piece is not None and piece.revealed:
                image_key = f"{piece.rank}_{'black' if piece.player == 1 else 'white'}"
                win.blit(PIECE_IMAGES[image_key], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def update_display(board):
    """
    Update the game display.

    Parameters:
    board (Board): The game board.
    """
    draw_board(WIN, board)
    draw_pieces(WIN, board)
    pygame.display.update()

def train_agents_with_display(num_episodes=10, max_steps=150, delay=0.2):
    """
    Train two AI agents with visual display.

    Parameters:
    num_episodes (int): Number of training episodes.
    max_steps (int): Maximum steps per episode.
    delay (float): Delay between steps for visualization.
    """
    ai_agent_1 = QLearningAgent(actions=['flip', 'move'], player=1)
    ai_agent_2 = QLearningAgent(actions=['flip', 'move'], player=2)

    # load previous Q-tables
    try:
        ai_agent_1.load_q_table('ai_agent_1_q_table.pkl')
        ai_agent_2.load_q_table('ai_agent_2_q_table.pkl')
        print("Q-tables loaded successfully.")
    except FileNotFoundError:
        print("No previous Q-tables found, starting fresh.")

    for episode in range(num_episodes):
        board = Board()
        state_1 = ai_agent_1.get_state(board)
        state_2 = ai_agent_2.get_state(board)
        done = False
        step_count = 0
        while not done and step_count < max_steps:
            # AI 1 takes action
            action_1 = ai_agent_1.choose_action(state_1, board)
            next_state_1, reward_1, done_1, action_detail_1 = ai_agent_1.step(state_1, action_1, board, step_count)
            ai_agent_1.update_q_table(state_1, action_1, reward_1, next_state_1)

            # Update display and sleep
            update_display(board)
            time.sleep(delay)

            if done_1:
                break

            # AI 2 takes action
            action_2 = ai_agent_2.choose_action(state_2, board)
            next_state_2, reward_2, done_2, action_detail_2 = ai_agent_2.step(state_2, action_2, board, step_count)
            ai_agent_2.update_q_table(state_2, action_2, reward_2, next_state_2)

            # Update display and sleep
            update_display(board)
            time.sleep(delay)

            # Update states and check if the game is done
            state_1 = next_state_1
            state_2 = next_state_2
            done = done_1 or done_2

            step_count += 1

        if (episode + 1) % 1000 == 0:
            print(f"Episode {episode + 1}/{num_episodes} completed")

    ai_agent_1.save_q_table('ai_agent_1_q_table.pkl')
    ai_agent_2.save_q_table('ai_agent_2_q_table.pkl')

if __name__ == "__main__":
    train_agents_with_display()
    pygame.quit()
    sys.exit()
