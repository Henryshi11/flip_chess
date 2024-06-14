# game.py
# Author: Henry Shi

import pygame
import sys
from board import Board
from qlearning_agent import QLearningAgent
from minmax_agent import MinMaxAgent

# Define colors
WHITE, BLACK, BLUE, RED, LIGHT_BLUE = (255, 255, 255), (0, 0, 0), (0, 0, 255), (255, 0, 0), (173, 216, 230)

# Load piece images (example)
PIECE_IMAGES = {
    'K_black': pygame.transform.scale(pygame.image.load('../images/king_black.png'), (100, 100)),
    'K_white': pygame.transform.scale(pygame.image.load('../images/king_white.png'), (100, 100)),
    'Q_black': pygame.transform.scale(pygame.image.load('../images/queen_black.png'), (100, 100)),
    'Q_white': pygame.transform.scale(pygame.image.load('../images/queen_white.png'), (100, 100)),
    'R_black': pygame.transform.scale(pygame.image.load('../images/rook_black.png'), (100, 100)),
    'R_white': pygame.transform.scale(pygame.image.load('../images/rook_white.png'), (100, 100)),
    'B_black': pygame.transform.scale(pygame.image.load('../images/bishop_black.png'), (100, 100)),
    'B_white': pygame.transform.scale(pygame.image.load('../images/bishop_white.png'), (100, 100)),
    'N_black': pygame.transform.scale(pygame.image.load('../images/knight_black.png'), (100, 100)),
    'N_white': pygame.transform.scale(pygame.image.load('../images/knight_white.png'), (100, 100)),
    'P_black': pygame.transform.scale(pygame.image.load('../images/pawn_black.png'), (100, 100)),
    'P_white': pygame.transform.scale(pygame.image.load('../images/pawn_white.png'), (100, 100)),
}

def draw_board(win, board):
    """
    Draw the game board.

    Parameters:
    win (pygame.Surface): The game window.
    board (Board): The game board.
    """
    win.fill(WHITE)
    for row in range(4):
        for col in range(8):
            color = LIGHT_BLUE if board.grid[row][col] is not None and not board.grid[row][col].revealed else (BLUE if (row + col) % 2 == 0 else RED)
            pygame.draw.rect(win, color, (col * 100, row * 100, 100, 100))
            pygame.draw.rect(win, BLACK, (col * 100, row * 100, 100, 100), 1)

def draw_pieces(win, board):
    """
    Draw the pieces on the board.

    Parameters:
    win (pygame.Surface): The game window.
    board (Board): The game board.
    """
    for row in range(4):
        for col in range(8):
            piece = board.grid[row][col]
            if piece is not None and piece.revealed:
                image_key = f"{piece.rank}_{'black' if piece.player == 1 else 'white'}"
                if image_key in PIECE_IMAGES:
                    win.blit(PIECE_IMAGES[image_key], (col * 100, row * 100))
                else:
                    print(f"Image for {image_key} not found in PIECE_IMAGES dictionary")

def get_square_under_mouse():
    """
    Get the board square under the mouse pointer.

    Returns:
    tuple: The row and column of the square, or None if out of bounds
    """
    mouse_pos = pygame.mouse.get_pos()
    x, y = mouse_pos[0] // 100, mouse_pos[1] // 100
    if 0 <= x < 8 and 0 <= y < 4:
        return (y, x)
    return None

def display_message(win, message):
    """
    Display a message in the game window.

    Parameters:
    win (pygame.Surface): The game window.
    message (str): The message to display.
    """
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, RED)
    text_rect = text.get_rect(center=(400, 200))
    win.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)

def draw_last_action(win, last_action):
    """
    Draw the last action taken by the AI.

    Parameters:
    win (pygame.Surface): The game window.
    last_action (str): The last action taken by the AI.
    """
    font = pygame.font.Font(None, 24)
    text = font.render(f"AI's last action: {last_action}", True, BLACK)
    win.blit(text, (10, 370))

def play_game(win, ai_type):
    """
    Play the game with the specified AI type.

    Parameters:
    win (pygame.Surface): The game window.
    ai_type (str): The type of AI to play against ('qlearning' or 'minmax').
    """
    board = Board()
    if ai_type == 'qlearning':
        ai_agent = QLearningAgent(actions=['flip', 'move'], player=2)
        ai_agent.load_q_table('ai_agent_1_q_table.pkl')
    elif ai_type == 'minmax':
        ai_agent = MinMaxAgent(depth=3, player=2)

    clock = pygame.time.Clock()
    selected_piece = None
    run = True
    player_turn = True
    player_color = 1
    step_count = 0
    last_action = "None"

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = get_square_under_mouse()
                if pos and player_turn:
                    row, col = pos
                    piece = board.grid[row][col]
                    if piece and not piece.revealed:
                        piece.reveal()
                        player_turn = False
                        step_count += 1
                    elif piece and piece.revealed and piece.player == player_color and not selected_piece:
                        selected_piece = (row, col)
                    elif selected_piece:
                        to_pos = pos
                        if board.is_valid_move(selected_piece, to_pos):
                            board.move_piece(selected_piece, to_pos)
                            player_turn = False
                            selected_piece = None
                            step_count += 1
                        elif board.is_valid_capture(selected_piece, to_pos):
                            board.capture_piece(selected_piece, to_pos)
                            player_turn = False
                            selected_piece = None
                            step_count += 1
                        else:
                            display_message(win, "Invalid move!")
                            selected_piece = None

        if not player_turn:
            state = ai_agent.get_state(board) if ai_type == 'qlearning' else None
            action = ai_agent.choose_action(board, step_count) if ai_type == 'minmax' else ai_agent.choose_action(state, board)
            if ai_type == 'qlearning':
                next_state, reward, done, action_detail = ai_agent.step(state, action, board, step_count)
            else:
                if action[0] == 'reveal':
                    _, pos = action
                    board.grid[pos[0]][pos[1]].reveal()
                    action_detail = f"flip piece at {pos}"
                else:
                    from_pos, to_pos = action
                    if board.is_valid_move(from_pos, to_pos):
                        board.move_piece(from_pos, to_pos)
                    elif board.is_valid_capture(from_pos, to_pos):
                        board.capture_piece(from_pos, to_pos)
                    action_detail = f"moved piece from {from_pos} to {to_pos}"
            last_action = action_detail
            player_turn = True
            step_count += 1

        draw_board(win, board)
        draw_pieces(win, board)
        draw_last_action(win, last_action)
        pygame.display.update()
        clock.tick(60)

        winner = board.check_winner(step_count)
        if winner is not None:
            if winner == 1:
                display_message(win, "Player 1 wins!")
            elif winner == 2:
                display_message(win, "Player 2 wins!")
            else:
                display_message(win, "Draw!")
            run = False

    pygame.quit()
    sys.exit()
