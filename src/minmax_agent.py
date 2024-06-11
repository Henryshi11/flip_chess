# minmax_agent.py
# Author: Henry Shi

import copy

class MinMaxAgent:
    def __init__(self, depth=3, player=1):
        self.depth = depth
        self.player = player

    def evaluate_board(self, board):
        """
        Evaluate the board and return a score based on the state.
    
        Parameters:
        board (Board): The board object
    
        Returns:
        int: The evaluation score
        """
        rank_values = {'K': 10, 'Q': 7, 'R': 5, 'B': 4, 'N': 2.5, 'P': 1}
        player_score = 0
        opponent_score = 0
    
        for row in board.grid:
            for piece in row:
                if piece:
                    if piece.player == self.player:
                        player_score += rank_values[piece.rank]
                    else:
                        opponent_score += rank_values[piece.rank]
                    
        return player_score - opponent_score


    def get_all_valid_moves(self, board, player):
        """
        Get all valid moves for the given player.

        Parameters:
        board (Board): The board object
        player (int): The player number

        Returns:
        list: A list of valid moves (from_pos, to_pos)
        """
        valid_moves = []
        for row in range(4):
            for col in range(8):
                piece = board.grid[row][col]
                if piece and piece.player == player and piece.revealed:
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        to_pos = (row + dr, col + dc)
                        if 0 <= to_pos[0] < 4 and 0 <= to_pos[1] < 8:
                            if board.is_valid_move((row, col), to_pos) or board.is_valid_capture((row, col), to_pos):
                                valid_moves.append(((row, col), to_pos))
        return valid_moves

    def get_all_unrevealed_positions(self, board):
        """
        Get all positions of unrevealed pieces.

        Parameters:
        board (Board): The board object

        Returns:
        list: A list of positions with unrevealed pieces
        """
        unrevealed_positions = []
        for row in range(4):
            for col in range(8):
                piece = board.grid[row][col]
                if piece and not piece.revealed:
                    unrevealed_positions.append((row, col))
        return unrevealed_positions

    def minimax(self, board, depth, maximizing_player, step_count):
        """
        Minimax algorithm to find the best move.

        Parameters:
        board (Board): The board object
        depth (int): The depth of the search
        maximizing_player (bool): Whether the current player is the maximizing player

        Returns:
        tuple: Best score and best move (score, move)
        """
        winner = board.check_winner(step_count)
        if winner == self.player:
            return 80, None
        elif winner == 3 - self.player:
            return -80, None
        elif winner == 0:
            return 0, None

        if depth == 0:
            return self.evaluate_board(board), None

        valid_moves = self.get_all_valid_moves(board, self.player if maximizing_player else 3 - self.player)

        if valid_moves:
            if maximizing_player:
                max_eval = float('-inf')
                best_move = None
                for move in valid_moves:
                    from_pos, to_pos = move
                    new_board = copy.deepcopy(board)
                    if new_board.is_valid_move(from_pos, to_pos):
                        new_board.move_piece(from_pos, to_pos)
                    elif new_board.is_valid_capture(from_pos, to_pos):
                        new_board.capture_piece(from_pos, to_pos)
                    eval, _ = self.minimax(new_board, depth - 1, False, step_count + 1)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = move
                return max_eval, best_move
            else:
                min_eval = float('inf')
                best_move = None
                for move in valid_moves:
                    from_pos, to_pos = move
                    new_board = copy.deepcopy(board)
                    if new_board.is_valid_move(from_pos, to_pos):
                        new_board.move_piece(from_pos, to_pos)
                    elif new_board.is_valid_capture(from_pos, to_pos):
                        new_board.capture_piece(from_pos, to_pos)
                    eval, _ = self.minimax(new_board, depth - 1, True, step_count + 1)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = move
                return min_eval, best_move
        else:
            if not board.all_pieces_revealed():
                unrevealed_positions = self.get_all_unrevealed_positions(board)
                if not unrevealed_positions:
                    return self.evaluate_board(board), None
                
                best_score = float('-inf') if maximizing_player else float('inf')
                best_move = None
                for pos in unrevealed_positions:
                    new_board = copy.deepcopy(board)
                    new_board.grid[pos[0]][pos[1]].reveal()
                    eval, _ = self.minimax(new_board, depth - 1, not maximizing_player, step_count + 1)
                    if maximizing_player:
                        if eval > best_score:
                            best_score = eval
                            best_move = ('reveal', pos)
                    else:
                        if eval < best_score:
                            best_score = eval
                            best_move = ('reveal', pos)
                return best_score, best_move

        return 0, None

    def choose_action(self, board, step_count):
        """
        Choose the best action for the current player.

        Parameters:
        board (Board): The board object
        step_count (int): The current step count

        Returns:
        tuple: The best move (action, pos)
        """
        _, best_move = self.minimax(board, self.depth, True, step_count)
        return best_move
