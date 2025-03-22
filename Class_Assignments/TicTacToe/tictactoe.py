# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 10:53:15 2024
@author: Alison Bean de Hernandez
"""

# Create a tic tac toe game with 2-players and 9-spaces game board
# Steps 
    # 1. Print the game board
    # 2. Have players submit selection 
    # 3. Check if player has won or tied or not
    # 4. Let other player make move
    # 5. Repeat until someone wins
    # 6. Close after win


#Setting specfic variables for the functions
game_board = ["A1", "B1", "C1",
              "A2", "B2", "C2",
              "A3", "B3", "C3"]

current_player = "X"
winner = None
game_active = True


# 1. Look at the game baord
def print_board(game_board):
    print(game_board[0] + "|" + game_board[1] + "|" + game_board[2])
    print("---------")
    print(game_board[3] + "|" + game_board[4] + "|" + game_board[5])
    print("---------")
    print(game_board[6] + "|" + game_board[7] + "|" + game_board[8])
    print(" ")


# 2. Have players submit selection 
def play_game(game_board):
    valid = False
    while valid ==False:
        position = input( "Choose a position: " ).upper()   
        if position == "A1":
            if game_board[0] == "A1":
                game_board[0] = current_player
                valid = True
        elif position == "A2": 
            if game_board[3] == "A2":
                game_board[3] = current_player
                valid = True
        elif position == "A3": 
             if game_board[6] == "A3":
                game_board[6] = current_player
                valid = True
        elif position == "B1" : 
             if game_board[1] == "B1":
                game_board[1] = current_player
                valid = True
        elif position == "B2": 
             if game_board[4] == "B2":
                game_board[4] = current_player
                valid = True
        elif position == "B3": 
            if game_board[7] == "B3":
                game_board[7] = current_player
                valid = True
        elif position == "C1": 
            if game_board[2] == "C1":
                game_board[2] = current_player
                valid = True
        elif position == "C2": 
            if game_board[5] == "C2":
                game_board[5] = current_player
                valid = True
        elif position == "C3": 
            if game_board[8] == "C3":
                game_board[8] = current_player
                valid = True
        if valid==False:
            print("Opps, that space is unavailable! Please try again.")
    return game_board


# 3. Check if player has won or not
def define_win(game_board): 
    global winner
    # Check rows
    if game_board[0] == game_board[1] == game_board[2]:
        winner = game_board[0]
        return True
    elif game_board[3] == game_board[4] == game_board[5]:
        winner = game_board[3]
        return True
    elif game_board[6] == game_board[7] == game_board[8]:
        winner = game_board[3]
        return True
    # Check Columns
    elif game_board[0] == game_board[3] == game_board[6]:
        winner = game_board[0]
        return True
    elif game_board[1] == game_board[4] == game_board[7]:
        winner = game_board[1]
        return True
    elif game_board[2] == game_board[5] == game_board[8]:
        winner = game_board[2]
        return True
    # Check diagonals
    elif game_board[0] == game_board[4] == game_board[8]:
        winner = game_board[0]
        return True
    elif game_board[2] == game_board[4] == game_board[6]:
        winner = game_board[2]
        return True
    
    
def check_win(game_board): 
    global game_active
    if define_win(game_board): 
        print_board(game_board)
        print(f"The winner is {winner}")
        game_active= False


def check_tie(game_board): 
    global game_active
    if game_board[0]!="A1" and game_board[1]!="B1" and game_board[2]!="C1" \
    and game_board[3]!="A2" and game_board[4]!="B2" and game_board[5]!="C2" \
    and game_board[6]!="A3" and game_board[7]!="B3" and game_board[8]!="C3": 
        print_board(game_board)
        print("It's a tie!")
        game_active= False
        

 # 4. Let other player make move
def switch_player(game_board):
    global current_player
    if current_player == "X" and winner == None: 
        current_player = "O" ### switch player
    else: 
        current_player = "X"
        

while game_active: 
    print_board(game_board)
    play_game(game_board)
    define_win(game_board)
    check_win(game_board)     ### checks rows, columns, and diagnols and then close when win occurs
    if game_active == True:   ### if all spaces are filled then it's a tie and should close the loop
        check_tie(game_board)
    switch_player(game_board) 
