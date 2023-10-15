"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # the logic will be as follows:
    #  count the number of X's and O's on the board
    #  if the number is equal then it's X's turn
    #  if X is one more than O then it's O's turn


    # variables to store the number of X's and O's
    x_count = 0
    o_count = 0


    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == X:
                x_count += 1
            elif board[row][col] == O:
                o_count += 1


    if x_count == o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # the logic will be as follows:
        #  check each cell in the board
        #  if the cell is empty save it to a list as row and column pair
        #  if not just continue to the next cell
        #  at the end return the list


    # a list to save the moves
    possible_moves = []

    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:

                # save the move to the list
                possible_moves.append((row, col))


    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # the logic will be as follows:
    #   check whose turn it is
    #   check if the action is valid
    #   if it is then save the move to the board
    #   return the new board

    # note that i will be copying the board to a different variable to avoid changing the original board
    # this is because this function will be used in the minimax function
    # and hence the algorithm will need to keep the same original board unchanged

    turn = player(board)

    valid = board[action[0]][action[1]] == EMPTY

    if valid:
        print("the move is valid")
        print(action)

        # note that i ran into some issues with the this line
        # since i wasn't creating a deepcopy of the board so it was getting full and then the game raises and invalid move exception because 
        # appearently the assignment operator in python just passes a reference to the original board in memory hence when we change the new variable it will change the old 
        # one thats why it didn't work
        # but deep copy creates a new object with a new memory address hence they don't interfere with each other
        new_board = copy.deepcopy(board)
        new_board[action[0]][action[1]] = turn
        print(board)
        print(new_board)
        return new_board
    else:
        raise Exception("Invalid move")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """


    # the logic will be as follows:
    #   check for horizontal lines
    #   check for vertical lines
    #   check for diagonal lines
    #   if none of the lines are found then the game is a tie or the game is still in progress which in both cases we should return None

    # check horizontal
    for row in range(len(board)):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != EMPTY:
            return board[row][0]
    
    # check vertical
    for col in range(len(board)):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]
        
    # check diagonal
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    

    # if either the game is not over yet or if the game is a tie then return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # we will call winner() if we get a value other than None
    # then we will know that it is over
    # however if we get None then we will check whether is is a tie or is it still in progress because 
    # there are two difference cases where we will get None back

    is_over = winner(board)
    if is_over is None:
        for row in range(len(board)):
            for col in range(len(board)):

                # if there is any empty cell then the game is still in progress
                # so we will return False
                if board[row][col] == EMPTY:
                    print("the board is not terminal")
                    return False
                
    # if we get here then the game is a tie or there is a winner so we will return true
    print("the board is terminal")
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # we were told that we can assume that this function will be called only if the game is over
    # this means that if terminal() returns None that is because 
    # so we can use the if statement to check for a winner
    # if the winner is X then we return 1
    # if the winner is O then we return -1

    win_player = winner(board)

    if win_player == X:
        return 1
    elif win_player == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # first we have to check whether this is a terminal board or not 
    # meaning is this already the end of the game or not
    if terminal(board):
        return None
    
    # if this is not a terminal board then we will check for the player
    turn = player(board)

    if turn == X:
        # if this is X then we will call the max_player function

        tmp = max_player(board)
        print(tmp)
        return tmp[0]
    else:
        # if this is O then we will call the min_player function
        print("it is O's turn i will start thinking")
        tmp = min_player(board)
        print(tmp)
        return tmp[0]



# both of the following functions return an action and a value in the form (action,value)
def min_player(board):
    # since this player wants to minimize the outcome then we will set the initial value to be a number larger then the highest possible
    # outcome which in this case is 1
    # in theory you would set the initial value to be infinity but since we now what is the highest possible result we will set it to be 1

    if terminal(board=board):
        print("Min terminal is true")
        return (None, utility(board=board))

    value = 10
    # since we will be returning the best action we have to keep track of the best action that we have seen 
    best_action = None

    # we will call the actions() function to get the possible moves
    for action in actions(board):
        print(f"min: action: {action}")

        action_value = max_player(result(board, action))[1]
        if action_value < value:
            value = action_value
            best_action = action

    return (best_action, value)

    


def max_player(board):
    # we will be reversing the logic of the min_player function
    if terminal(board=board):
        print("Max terminal is true")
        return (None, utility(board=board))
    
    value = -10

    best_action = None

    for action in actions(board):

        print(f"max: action: {action}")
        action_value = min_player(result(board, action))[1]
        if action_value > value:
            value = action_value
            best_action = action


    return (best_action, value)

