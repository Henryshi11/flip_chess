# qlearning_agent.py
# Author: Henry Shi

import numpy as np
import random
import pickle

class QLearningAgent:


    def __init__(self, alpha=0.3, gamma=0.8, epsilon=0.1, actions=None, player=1):
        self.alpha = alpha #Learning rate, 30% new data
        self.gamma = gamma #Discount factor, 80% future reward
        self.epsilon = epsilon #Exploration rate, 10% random move

        self.q_table = {}
        self.actions = actions if actions is not None else []
        self.player = player

    def get_state(self, board):
        """
        Get the state of the board.

        Parameters:
        board (Board): The board object

        Returns:
        tuple: A tuple representation of the board state
        """
        return tuple(tuple((piece.rank, piece.player, piece.revealed) if piece else None for piece in row) for row in board.grid)

    def choose_action(self, state, board):
        """
        Choose the best action based on the current state and epsilon-greedy policy.

        Parameters:
        state (tuple): The current state
        board (Board): The board object

        Returns:
        str: The chosen action
        """
        unflipped_positions = [(r, c) for r in range(len(board.grid)) for c in range(len(board.grid[0])) if board.grid[r][c] and not board.grid[r][c].revealed]
        valid_actions = self.actions if unflipped_positions else ['move']

        if np.random.rand() < self.epsilon:
            return np.random.choice(valid_actions)
        q_values = [self.q_table.get((state, action), 0) for action in valid_actions]
        return valid_actions[np.argmax(q_values)] if q_values else np.random.choice(valid_actions)

    def update_q_table(self, state, action, reward, next_state):
        """
        Update the Q-table using the Q-learning update rule.

        Parameters:
        state (tuple): The current state
        action (str): The action taken
        reward (int): The received reward
        next_state (tuple): The next state
        """
        old_q_value = self.q_table.get((state, action), 0)
        next_max_q_value = max([self.q_table.get((next_state, a), 0) for a in self.actions], default=0)
        new_q_value = old_q_value + self.alpha * (reward + self.gamma * next_max_q_value - old_q_value)
        self.q_table[(state, action)] = new_q_value

    def step(self, state, action, board, step_count):
        """
        Take a step in the environment based on the action and update the state.

        Parameters:
        state (tuple): The current state
        action (str): The action taken
        board (Board): The board object
        step_count (int): The current step count

        Returns:
        tuple: The next state, received reward, done flag, and action detail
        """
        reward = 0
        done = False
        action_detail = ""

        if action == 'flip':
            unflipped_positions = [(r, c) for r in range(len(board.grid)) for c in range(len(board.grid[0])) if board.grid[r][c] and not board.grid[r][c].revealed]
            if unflipped_positions:
                pos = random.choice(unflipped_positions)
                piece = board.grid[pos[0]][pos[1]]
                piece.reveal()
                reward = -1
                action_detail = f"flipped {piece.rank} at ({pos[0]}, {pos[1]})"
            else:
                action = 'move'

        if action == 'move':
            valid_moves = [(from_pos, to_pos) for from_pos in [(r, c) for r in range(len(board.grid)) for c in range(len(board.grid[0])) if board.grid[r][c] and board.grid[r][c].revealed and board.grid[r][c].player == self.player]
                           for to_pos in [(from_pos[0] + dr, from_pos[1] + dc) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]] if 0 <= to_pos[0] < 4 and 0 <= to_pos[1] < 8 and (board.is_valid_move(from_pos, to_pos) or board.is_valid_capture(from_pos, to_pos))]
            if valid_moves:
                from_pos, to_pos = random.choice(valid_moves)
                if board.grid[to_pos[0]][to_pos[1]] is None:
                    board.move_piece(from_pos, to_pos)
                    reward = -1
                    action_detail = f"moved piece from ({from_pos[0]}, {from_pos[1]}) to ({to_pos[0]}, {to_pos[1]})"
                else:
                    if board.is_valid_capture(from_pos, to_pos):
                        captured_piece = board.grid[to_pos[0]][to_pos[1]]
                        board.capture_piece(from_pos, to_pos)
                        reward = 4
                        action_detail = f"captured {captured_piece.rank} at ({to_pos[0]}, {to_pos[1]}) with piece from ({from_pos[0]}, {from_pos[1]})"
                    else:
                        reward = -1
                        done = True
            else:
                reward = -1
                done = True

        next_state = self.get_state(board)
        winner = board.check_winner(step_count)
        if winner is not None:
            if winner == self.player:
                reward += 80
            done = True

        return next_state, reward, done, action_detail

    def save_q_table(self, filename):
        """
        Save the Q-table to a file.

        Parameters:
        filename (str): The name of the file to save the Q-table
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename):
        """
        Load the Q-table from a file.

        Parameters:
        filename (str): The name of the file to load the Q-table from
        """
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)

    def update_q_table_from_experience(self, experiences):
        """
        Update the Q-table from a list of experiences.

        Parameters:
        experiences (list): A list of experiences (state, action, reward, next state)
        """
        for state, action, reward, next_state in experiences:
            self.update_q_table(state, action, reward, next_state)
