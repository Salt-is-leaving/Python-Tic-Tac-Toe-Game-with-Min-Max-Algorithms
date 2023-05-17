#%%

"""
\\\\\ Vier gewinnt /////

DAISY WS22/23

import numpy as np
import random


class Game:
    def __init__(self, m = 5, n = 5, k = 4, mode = 4 ):
        self.board = Board(m, n, k)
        player1bot = mode > 2 # Modi 3 & 4
        player2bot = (mode % 2 == 0) # Modi 1, 2 & 4
     
        if player1bot: #for Player1 
            self.player1 = MyBot(1) 
        else:
            self.player1 = Player(1) 
            
        if player2bot: #for Player2 
             self.player2 = MyBot(2) 
        else:
             self.player2 = Player(2) 
             
        self.current_player = self.player1

    def start(self):
        self.board.display()
        self.game_loop()


    def game_loop(self):
        while True:
            player_number = self.current_player.player_number
            
            # first checking if any move still left. If not, tie.
            if not self.board.has_moves():
                print("Tie! / Unentschieden!")
                self.board.display() 
                break
            
            # if there is a move left, let's get a move:
            print(f"\nPlayer {player_number}: Your turn, {self.current_player.name}!")            
            move = self.current_player.get_move(self.board) 
            print(f"Player {player_number} played row {move[0]+1}, col {move[1]+1}.") #for display purposes we use 1-based indexing
            
            # if the move is invalid (either taken or not in the range of the board),then continue the loop of getting a move
            if not self.board.is_valid(move):
                print("Invalid Move\n\n")
                continue

            # if the move is valid, then apply it & check whether the player has won:
            self.board.apply_move(move) #instead of self.board.array
            if  self.board.hasWonAfterMove(move):
                print(f"Player {player_number} has won.") 
                self.board.display()
                print(f"Congratulations, {self.current_player.name}!!")
                break
            else:
                print(f"Player {player_number} has not won yet.") 
                
            # switch players:
            if self.current_player == self.player1:
                self.current_player = self.player2
            elif self.current_player == self.player2:
                self.current_player = self.player1

            # display the board:
            self.board.display()
            


class Board:
    def __init__(self, m = 5, n = 5, k = 4):
        self.m = m
        self.n = n
        self.k = k
        self.fields_left = m * n
        self.array = np.zeros([self.m, self.n])

    def display(self):
        # to print a nice matrix:
        print("+"+"--+"*self.n)
        for row in range(self.m):
            rowToPrint = "|"
            for col in range(self.n):
                if self.array[row, col]:
                    tile = str(int(self.array[row, col]))
                else:
                    tile = " "
                rowToPrint += (tile + " |")
            print(rowToPrint)
            print("+"+"--+"*self.n)
            
        # to apply a valid move to the board: 
    def apply_move(self, move):
        row, col, player_number = move
        self.array[row, col] = player_number
        self.fields_left -= 1

        # to undo the move after we've evaluated the move before we finally choose the move:
    def unapply_move(self, move):
        row, col, player_number = move
        self.array[row, col] = 0
        self.fields_left += 1
        
        # checking if the move is valid: 
    def is_valid(self, move):
        row, col, player_number = move
        if row >= self.m or col >= self.n:
            return False
        if row < 0 or col < 0:
            return False
        return self.array[row, col] == 0

        # check whether any fields left to put a stone: 
    def has_moves(self):
        return self.fields_left > 0
    
        # creating a list of all valid moves:
    def possibleMoves(self, player_number):
        result = []
        for row in range(self.m):
            for col in range(self.n):
                move = row, col, player_number
                if self.is_valid(move):
                    result.append(move)
        return result
                    

        # checking whether a player won after the move has been applied:
    def hasWonAfterMove(self, move):
        row, col, player_number = move
        # horizontal: check the current row, starting from col 0, going to the right = 0, 1
        if self.maxStonesInSeq(player_number, row, 0, 0, 1) >= self.k:
            return True
        
        # vertical: check the current col, starting from row 0, going down = 1, 0
        if self.maxStonesInSeq(player_number, 0, col, 1, 0) >= self.k:
            return True
        
        # \-diagonal:
        # need to determine which diagonal we are on: 
        idxDiag = col - row # postive: above the main diag, neg: below
        
        # if positive, we start at that col, else at that row
        if idxDiag >= 0:
            startRow, startCol = 0, idxDiag
        else:
            startRow, startCol = -idxDiag, 0
            
        # diagonal right down: going right down = 1, 1
        if self.maxStonesInSeq(player_number, startRow, startCol, 1, 1) >= self.k:
            return True
        
        # /-diagonal: 
        idxDiag = (self.m - 1 - row) - col # postive above, negative below        

        if idxDiag >= 0: # above diagonal / need to start in col 0
            startRow, startCol = self.m - 1 - idxDiag, 0
        else: # below diagonal / need to start in the last row
            startRow, startCol = self.m - 1, -idxDiag
            
        # diagonal right up: going right up = -1, 1
        if self.maxStonesInSeq(player_number, startRow, startCol, -1, 1) >= self.k:
            return True
        return False

    def maxStonesInSeq(self, player_number, fromx, fromy, dx, dy):
        # dx can be 0 or 1, dy can be 0 or 1 or -1
        # we start at fromx, fromy and go in direction dx, dy as far as possible
        numSiS = 0 # number of stones in the sequence
        maxSiS = 0 # max number of stones in the sequence
        x, y = fromx, fromy
        while (x >= 0 and x < self.m) and (y >= 0 and y < self.n):
            if self.array[x,y] == player_number:
                numSiS += 1
                if numSiS > maxSiS:
                    maxSiS = numSiS
            else:
                numSiS = 0
            x += dx
            y += dy
        return maxSiS


class Player:
    def __init__(self, player_number):
        self.name = input(f"Player {player_number}, enter your name: ")
        self.player_number = player_number 
        
    def get_move(self, board):
        row = int(input("Which Row (starting from 1)?: "))
        col = int(input("Which Column (starting from 1)? : "))
        # people start counting with 1, so we subtract 1
        move = row-1, col-1, self.player_number
        return move
     

class MyBot:
    def __init__(self, player_number):
        self.player_number = player_number
        self.name = "Bot" + str(player_number)
        self.initial_depth = 5 

    def get_move(self, board):
        # we've checked above whether there is an available move
        move = self.best_move(board, self.player_number, self.initial_depth)
        return move
        
        # to evaluate all the moves & pick the best one: 
    def best_move(self, board, player_number, remaining_depth):
        possibleMoves = board.possibleMoves(player_number)
   
        # if we don't have search depth left, we evaluate the available moves & pick the best ones:
        if remaining_depth <= 1:
            best_score = -99999
            for move in possibleMoves:
                score = self.score_after_move(board, move)
                if score > best_score:
                    best_score = score
                    best_move = move
                    
        # otherwise for every possible move we check what opponnent can do best case & pick the move that makes the opponent score the worst: 
        else:
             worst_opponent_score = 99999
             for move in possibleMoves:
                board.apply_move(move)
                # if I have won: score is 1000, return winning move
                if board.hasWonAfterMove(move): # that's the best move
                    board.unapply_move(move)
                    return move
                # if it is a tie: score 0
                if not board.has_moves():
                    opponent_score = 0
                    
                # if we haven't won and it's not a tie, that is an opponnent's move which we evaluate and accordingly
                # we choose our next move in a way that makes an opponnet score the worst
                else:
                    opponent_player_number = 3 - player_number
                    opponent_move = self.best_move(board, opponent_player_number, remaining_depth - 1)
                    opponent_score = self.score_after_move(board, opponent_move)
                board.unapply_move(move)
                
                # pick the move with the smallest (worst) opponnent score:
                if opponent_score < worst_opponent_score:
                     worst_opponent_score = opponent_score
                     best_move = move
        return best_move #the best move for me


    def score_after_move(self, board, move):
        # +1000 is winning, -1000 is losing, 0 is tie
        board.apply_move(move) #apply the move temporary to check the whether it's a winning move
        hasWon = board.hasWonAfterMove(move)
        board.unapply_move(move) 
        if hasWon:
            return 1000
        else:
            return np.random.randint(100)
        

mode = int(input("Choose the game mode: human/human 1), human/bot 2), bot/human 3), bot/bot 4)"))
test_game = Game(5,5,4, mode)
test_game.start()
