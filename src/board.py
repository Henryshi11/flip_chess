# board.py
# Author: Henry Shi

import random

class Piece:
    def __init__(self, rank, player):
        """
        Initialize a piece.

        Parameters:
        rank (str): The rank of the piece (e.g., 'K' for King)
        player (int): The player to which the piece belongs (1 or 2)
        """
        self.rank = rank
        self.player = player
        self.revealed = False

    def reveal(self):
        """Reveal the piece."""
        self.revealed = True

class Board:
    def __init__(self):
        """Initialize the board with a 4x8 grid."""
        self.grid = [[None for _ in range(8)] for _ in range(4)]
        self.initialize_pieces()

    def initialize_pieces(self):
        """Randomly distribute the pieces on the board."""
        pieces = [
            ('K', 1), ('Q', 1), ('Q', 1), ('R', 1), ('R', 1), ('B', 1), ('B', 1), ('B', 1), ('N', 1), ('N', 1), ('N', 1), ('P', 1), ('P', 1), ('P', 1), ('P', 1), ('P', 1),
            ('K', 2), ('Q', 2), ('Q', 2), ('R', 2), ('R', 2), ('B', 2), ('B', 2), ('B', 2), ('N', 2), ('N', 2), ('N', 2), ('P', 2), ('P', 2), ('P', 2), ('P', 2), ('P', 2)
        ]
        random.shuffle(pieces)
        index = 0
        for row in range(4):
            for col in range(8):
                rank, player = pieces[index]
                self.grid[row][col] = Piece(rank, player)
                index += 1

    def move_piece(self, from_pos, to_pos):
        """
        Move a piece from one position to another.

        Parameters:
        from_pos (tuple): The starting position
        to_pos (tuple): The ending position
        """
        if self.is_valid_move(from_pos, to_pos):
            self.grid[to_pos[0]][to_pos[1]] = self.grid[from_pos[0]][from_pos[1]]
            self.grid[from_pos[0]][from_pos[1]] = None

    def capture_piece(self, from_pos, to_pos):
        """
        Capture a piece from one position to another.

        Parameters:
        from_pos (tuple): The starting position
        to_pos (tuple): The ending position
        """
        from_piece = self.grid[from_pos[0]][from_pos[1]]
        to_piece = self.grid[to_pos[0]][to_pos[1]]
        if self.is_valid_capture(from_pos, to_pos):
            if from_piece.rank == to_piece.rank:
                self.grid[from_pos[0]][from_pos[1]] = None
                self.grid[to_pos[0]][to_pos[1]] = None
            else:
                self.grid[to_pos[0]][to_pos[1]] = from_piece
                self.grid[from_pos[0]][from_pos[1]] = None

    def is_valid_move(self, from_pos, to_pos):
        """
        Check if a move is valid.

        Parameters:
        from_pos (tuple): The starting position
        to_pos (tuple): The ending position

        Returns:
        bool: Whether the move is valid
        """
        if self.grid[from_pos[0]][from_pos[1]] is None:
            return False
        if self.grid[to_pos[0]][to_pos[1]] is not None:
            return False
        row_diff = abs(from_pos[0] - to_pos[0])
        col_diff = abs(from_pos[1] - to_pos[1])
        return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)

    def is_valid_capture(self, from_pos, to_pos):
        """
        Check if a capture is valid.

        Parameters:
        from_pos (tuple): The starting position
        to_pos (tuple): The ending position

        Returns:
        bool: Whether the capture is valid
        """
        if self.grid[from_pos[0]][from_pos[1]] is None or self.grid[to_pos[0]][to_pos[1]] is None:
            return False
        from_piece = self.grid[from_pos[0]][from_pos[1]]
        to_piece = self.grid[to_pos[0]][to_pos[1]]
        if not to_piece.revealed:  # Ensure the target piece is revealed
            return False
        if from_piece.player == to_piece.player:
            return False
        row_diff = abs(from_pos[0] - to_pos[0])
        col_diff = abs(from_pos[1] - to_pos[1])
        if not ((row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)):
            return False
        rank_order = {'K': 6, 'Q': 5, 'R': 4, 'B': 3, 'N': 2, 'P': 1}
        if from_piece.rank == 'K' and to_piece.rank == 'P':
            return False  # King cannot capture Pawn
        if from_piece.rank == 'K':
            return rank_order[to_piece.rank] < 7  # King can capture anything except Pawns
        elif from_piece.rank == 'Q':
            return rank_order[to_piece.rank] < 6  # Queen can capture anything except Kings
        elif from_piece.rank == 'R':
            return rank_order[to_piece.rank] < 5  # Rook can capture anything except Kings and Queens
        elif from_piece.rank == 'B':
            return rank_order[to_piece.rank] < 4  # Bishop can capture anything except Kings, Queens, and Rooks
        elif from_piece.rank == 'N':
            return rank_order[to_piece.rank] < 3  # Knight can capture anything except Kings, Queens, Rooks, and Bishops
        elif from_piece.rank == 'P':
            return to_piece.rank == 'K' or to_piece.rank == 'P'  # Pawn can only capture Kings and other Pawns
        return False

    def all_pieces_revealed(self):
        """
        Check if all pieces on the board have been revealed.

        Returns:
        bool: True if all pieces are revealed, False otherwise.
        """
        for row in self.grid:
            for piece in row:
                if piece and not piece.revealed:
                    return False
        return True

    def get_state(self):
        """
        Get the current state of the board.

        Returns:
        tuple: A tuple representation of the board state
        """
        return tuple(tuple((piece.rank, piece.player, piece.revealed) if piece else None for piece in row) for row in self.grid)

    def check_winner(self, step_count):
        """
        Check if there is a winner.

        Parameters:
        step_count (int): The current step count

        Returns:
        int: The player who won, or 0 for a draw, or None if no winner yet
        """
        if not self.all_pieces_revealed():
            return None  # Do not check winner if all pieces are not revealed

        player1_pieces = 0
        player2_pieces = 0
        player1_has_moves = False
        player2_has_moves = False
        for row in range(4):
            for col in range(8):
                piece = self.grid[row][col]
                if piece is not None:
                    if piece.player == 1:
                        player1_pieces += 1
                        if any(self.is_valid_move((row, col), (row + dr, col + dc)) for dr in (-1, 1) for dc in (0, 0) if 0 <= row + dr < 4 and 0 <= col + dc < 8):
                            player1_has_moves = True
                        if any(self.is_valid_move((row, col), (row, col + dc)) for dr in (0, 0) for dc in (-1, 1) if 0 <= row < 4 and 0 <= col + dc < 8):
                            player1_has_moves = True
                        if any(self.is_valid_capture((row, col), (row + dr, col + dc)) for dr in (-1, 1) for dc in (0, 0) if 0 <= row + dr < 4 and 0 <= col + dc < 8):
                            player1_has_moves = True
                        if any(self.is_valid_capture((row, col), (row, col + dc)) for dr in (0, 0) for dc in (-1, 1) if 0 <= row < 4 and 0 <= col + dc < 8):
                            player1_has_moves = True
                    elif piece.player == 2:
                        player2_pieces += 1
                        if any(self.is_valid_move((row, col), (row + dr, col + dc)) for dr in (-1, 1) for dc in (0, 0) if 0 <= row + dr < 4 and 0 <= col + dc < 8):
                            player2_has_moves = True
                        if any(self.is_valid_move((row, col), (row, col + dc)) for dr in (0, 0) for dc in (-1, 1) if 0 <= row < 4 and 0 <= col + dc < 8):
                            player2_has_moves = True
                        if any(self.is_valid_capture((row, col), (row + dr, col + dc)) for dr in (-1, 1) for dc in (0, 0) if 0 <= row + dr < 4 and 0 <= col + dc < 8):
                            player2_has_moves = True
                        if any(self.is_valid_capture((row, col), (row, col + dc)) for dr in (0, 0) for dc in (-1, 1) if 0 <= row < 4 and 0 <= col + dc < 8):
                            player2_has_moves = True

        if player1_pieces == 0:
            return 2  # Player 2 wins
        elif player2_pieces == 0:
            return 1  # Player 1 wins
        elif not player1_has_moves:
            return 2  # Player 2 wins if Player 1 has no moves
        elif not player2_has_moves:
            return 1  # Player 1 wins if Player 2 has no moves
        elif step_count >= 150:
            player1_score = self.calculate_score(1)
            player2_score = self.calculate_score(2)
            if player1_score > player2_score:
                return 1
            elif player2_score > player1_score:
                return 2
            else:
                return 0  # Draw

        return None  # No winner yet

    def calculate_score(self, player):
        """
        Calculate the score for a player.

        Parameters:
        player (int): The player number (1 or 2)

        Returns:
        int: The calculated score
        """
        score = 0
        rank_values = {'K': 10, 'Q': 7, 'R': 5, 'B': 4, 'N': 2.5, 'P': 1}
        for row in self.grid:
            for piece in row:
                if piece and piece.player == player:
                    score += rank_values[piece.rank]
        return score
