"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Edge board and near edge moves have less possible moves. So they should be
    have different score value. It's close to center_score heuristic, but it doesn't differ
    all centered moves that not close to edge. Cuz all centered moves have same amount of freedoms
    (possible moves) they should not be differ.
    Edge move value = 1
    Near edge move value = 2
    All centered moves value = 3

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    own_moves_value = 0
    opp_moves_value = 0

    board_width = game.width
    board_height = game.height

    for move in own_moves:
        # check if edge move
        if 0 in move or move[0] == board_width - 1 or move[1] == board_height - 1:
            own_moves_value += 1
        # check if near edge move
        elif 1 in move or move[0] == board_width - 2 or move[1] == board_height - 2:
            own_moves_value += 2
        else:
            own_moves_value += 3

    return float(own_moves_value - opp_moves_value)


def custom_score_2(game, player):
    """Heuristic build on board of values for possible moves. Value of each move = number of possible moves
    main idea, that only close to corner move have less that 8 possible moves. Even changing board size
    will have same nubmer of possible moves for corners, closest corner siblings, edge  moves etc. And all
    center moves that are more than 2 cells from edge will allways have 8 possible moves

    8х8 board example:
    
    2 3 4 4 4 4 3 2
    3 4 6 6 6 6 4 3
    4 6 8 8 8 8 6 4
    4 6 8 8 8 8 6 4
    4 6 8 8 8 8 6 4
    4 6 8 8 8 8 6 4
    3 4 6 6 6 6 4 3
    2 3 4 4 4 4 3 2

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    board_width = game.width
    board_height = game.height

    moves = game.get_legal_moves(player)
    moves_value = 0

    # 
    for move in moves:
        if move[0] == 0 or move[0] == board_width - 1:
            if move[1] == 0 or move[1] == board_height - 1:
                moves_value += 2
            elif move[1] == 1 or move[1] == board_height - 2:
                moves_value += 3
            else:
                moves_value += 4
        elif move[0] == 1 or move[0] == board_width - 2:
            if move[1] == 0 or move[1] == board_height - 1:
                moves_value += 3
            elif move[1] == 1 or move[1] == board_height - 2:
                moves_value += 4
            else:
                moves_value += 6
        elif move[1] == 0 or move[1] == board_height - 1:
            moves_value += 4
        elif move[1] == 1 or move[1] == board_height - 2:            
            moves_value += 6
        else:          
            moves_value += 8

    return float(moves_value)


def custom_score_3(game, player):
    """Heuristic build on board of values for possible moves + difference with second player 

    2 3 4 4 4 4 3 2
    3 4 6 6 6 6 4 3
    4 6 8 8 8 8 6 4
    4 6 8 8 8 8 6 4
    4 6 8 8 8 8 6 4
    4 6 8 8 8 8 6 4
    3 4 6 6 6 6 4 3
    2 3 4 4 4 4 3 2

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    board_width = game.width
    board_height = game.height

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    own_moves_value = 0
    opp_moves_value = 0

    def count_move_value(move):
        value = 0

        if move[0] == 0 or move[0] == board_width - 1:
            if move[1] == 0 or move[1] == board_height - 1:
                value = 2
            elif move[1] == 1 or move[1] == board_height - 2:
                value = 3
            else:
                value = 4
        elif move[0] == 1 or move[0] == board_width - 2:
            if move[1] == 0 or move[1] == board_height - 1:
                value = 3
            elif move[1] == 1 or move[1] == board_height - 2:
                value = 4
            else:
                value = 6
        elif move[1] == 0 or move[1] == board_height - 1:
            value = 4
        elif move[1] == 1 or move[1] == board_height - 2:            
            value = 6
        else:          
            value = 8

        return value

    for move in own_moves:
        own_moves_value += count_move_value(move)

    for move in opp_moves:
        opp_moves_value += count_move_value(move)

    return float(own_moves_value - opp_moves_value)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score_3, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        def min_value(game, depth):
            # return 1 if current game state is - winning state, otherwise call max_value
            # on every possible move
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            # if not bool(game.get_legal_moves()):
            #     return 1

            if depth == 0 or not bool(game.get_legal_moves()):
                return self.score(game, self)

            infinity = float("inf")

            for move in game.get_legal_moves():
                value = min(infinity, max_value(game.forecast_move(move), depth - 1))

            return value


        def max_value(game, depth):
            # return -1 if current game state is - losing state, otherwise call min_value
            # on every possible move
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            # if not bool(game.get_legal_moves()):
            #     return -1

            if depth == 0 or not bool(game.get_legal_moves()):
                return self.score(game, self)

            min_infinity = float("-inf")

            for move in game.get_legal_moves():
                value = max(min_infinity, min_value(game.forecast_move(move), depth - 1))

            return value


        if (not bool(game.get_legal_moves())):
            return (-1, -1)
 
        return max(game.get_legal_moves(), key=lambda move: min_value(game.forecast_move(move), depth - 1))


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        depth = 1

        while True:
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.
                best_move = self.alphabeta(game, depth)
                depth += 1

            except SearchTimeout:
                break  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        def min_value(game, depth, alpha, beta):
            # return 1 if current game state is - winning state, otherwise call max_value
            # on every possible move
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            depth -= 1

            if depth <= 0:
                return self.score(game, self)

            value = float("inf")

            for move in game.get_legal_moves():
                value = min(value, max_value(game.forecast_move(move), depth, alpha, beta))
                if value <= alpha:
                    return value
                beta = min(beta, value)

            return value


        def max_value(game, depth, alpha, beta):
            # return -1 if current game state is - losing state, otherwise call min_value
            # on every possible move
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            depth -= 1

            if depth <= 0:
                return self.score(game, self)

            value = float("-inf")

            for move in game.get_legal_moves():
                value = max(value, min_value(game.forecast_move(move), depth, alpha, beta))
                if value >= beta:
                    return value
                alpha = max(alpha, value)

            return value

        legal_moves = game.get_legal_moves()
        best_move = (-1, -1)
        value = float("-inf")

        if (not bool(legal_moves)):
            return best_move

        for move in legal_moves:
            new_value = min_value(game.forecast_move(move), depth, alpha, beta)
            if new_value > value:
                value = new_value
                best_move = move

            alpha = max(alpha, value)

        return best_move


