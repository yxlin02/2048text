import random as rd
import os
import copy

class GameBoard:
    def __init__(self, width = 4, height = 4, win_number = 2048):
        """ The constructor method that construct instance variable.
        """
        self.width = width
        self.height = height
        self.win_number = win_number
        #the game is in a 4*4 matrix and the winning score is 2048
        #the matrix is stored as a big list of each row containing small lists of each block(column)
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        #set every block in the matrix to 0
        self.reset()
    
    def reset(self):
        """ The function that reset the game and generate two random block of number
        """
        self.score = 0
        #generate two cells to start the game
        self.generate()
        self.generate()

    def generate(self):
        """This function choose a random empty block and generate 2 or 4 as new number
        """
        #80% chance generate 2 as new block number, 20% generare 2 as new block number
        number = 4
        if rd.randint(1,100) < 80:
        
            number = 2
        #the list empty_cells contains every block that is empty (without a number)
        empty_cells = []
        for row in range(self.height):
            for col in range(self.width):
                #this loop go through every block in the matrix
                if self.field[row][col] == 0: #the block is empty
                    empty_cells.append([row,col])
        #if empty_cells contains a block, the random number will be generated to 
        #a random empty block chosen from the empty_cells list
        if empty_cells:
            cell = rd.choice(empty_cells)
            self.field[cell[0]][cell[1]] = number
    
    def check_win(self):
        """This function checks the winning state of the game
        """
        for row in range(self.height):
            for col in range(self.width):
                if self.field[row][col] == self.win_number:
                    #if any block reach the win_number (2048), the player wins the game
                    return True
        return False
    
    def check_loss(self):
        """This function checks the losing state of the game. If there is 
        no more movement avaliable, the player lose the game
        """
        lose = True
        for direction in ["LEFT", "RIGHT", "UP", "DOWN"]:
            if self.movable_in_direction(direction) == True:
                lose = False
        return lose

    def movable_in_direction(self, direction):
        """ This function checks if it is movable in a certain direction
        Parameter: 
            :param direction: a string indicating the direction of movement 
        """
        # two helper function are used to make the code more efficient (only one check function is needed)
        if direction == "LEFT":
            check_field = self.field
        if direction == "RIGHT":
            #invert_row_in_field will invert every row (1234 becomes 4321)
            #check left 4321 is the same as 1234 check right
            check_field = self.invert_row_in_field(self.field)
        if direction == "UP":
            #This is similar to invert but it switches column and row
            #after rotating row and column, check left of the new field is the 
            #same as check up of the old field 
            check_field = self.rotate_row_col(self.field)
        if direction == "DOWN":
            #To check down, the field need to be rotated then inverted
            check_field = self.invert_row_in_field(self.rotate_row_col(self.field))
        #the new field is check to the right
        return self.check_left_movable_in_field(check_field)
        
    def rotate_row_col(self, field):
        """This function rotate the column and row
        Parameters:
            :param field: the field list that is a big list of each row containing small lists of each block(column)
        """
        new_width = len(field)
        new_height = len(field[0])
        rotated_field = [[0 for i in range(new_width)] for j in range(new_height)]
        for row in range(new_height):
            for col in range(new_width):
                #this function switches the row and colum in the list
                rotated_field[row][col] = field[col][row]
        return rotated_field

    def invert_row_in_field(self, field):
        """This function reverse each block in each row in the entire board (make 1234 to 4321)
        Parameters:
            :param field: the field list that is a big list of each row containing small lists of each block(column)
        """
        inverted_field = copy.deepcopy(field)
        for row in inverted_field:
            row.reverse()
        return inverted_field

    def check_left_movable_in_field(self, field):
        """This function returns a boolean on rather the current field is movable or not
        Parameters:
            :param field: the field list that is a big list of each row containing small lists of each block(column)
        """
        movable = False
        for row in field:
            if self.left_movable_in_row(row) == True:
                movable = True
        return movable

    def left_movable_in_row(self, row):
        """This function checks on rather each row is movable to the left or not
        Parameters:
            :param field: the field list that is a big list of each row containing small lists of each block(column)
        """
        for i in range(len(row)-1):
            if row[i] == 0 and row[i + 1] !=0:
                #if there is an empty block to the left of an occupied block, it is movable to left
                return True
            if row[i] != 0 and row[i] == row[i + 1]:
                #if there are two blocks next to each other with same number, it is movable
                return True
        return False
    
    def move(self, direction):
        """This function moves each block to the indicated direction
        Parameters:
            :param direction: a string indicating the moving direction
        """
        #in order to not write a function for each direction, invert and rotate function are
        #again used to make moving left equivilent to moving to any direction
        if direction == "LEFT":
            for row in range(self.height):
                new_row = self.move_row_left(self.field[row])
                self.field[row] = new_row
        if direction == "RIGHT":
            temp_field = self.invert_row_in_field(self.field)
            for row in range(self.height):
                temp_field[row] = self.move_row_left(temp_field[row])
            self.field = self.invert_row_in_field(temp_field)
        if direction == "UP":
            temp_field = self.rotate_row_col(self.field)
            for row in range(self.width):
                temp_field[row] = self.move_row_left(temp_field[row])
            self.field = self.rotate_row_col(temp_field)
        if direction == "DOWN":
            temp_field = self.invert_row_in_field(self.rotate_row_col(self.field))
            for row in range(self.width):
                temp_field[row] = self.move_row_left(temp_field[row])
            self.field = self.rotate_row_col(self.invert_row_in_field(temp_field))
        #after moving, generate a new number
        self.generate()

    def move_row_left(self, row):
        """This function move the row to left
        Paramters:
            :param row: a list that contains each item in the 4 blocks
        """
        #to move the row correctly, first the row is tightened to left
        #then the same numbers are merged
        #after merging, the row is tightened again
        new_row = self.tighten_row(row)
        new_row = self.merge_row(new_row)
        new_row = self.tighten_row(new_row)
        return new_row

    def tighten_row(self, row):
        """This functions tighten the row, that is, move all occupied block to the left
        Paramters:
            :param row: a list that contains each item in the 4 blocks
        """
        new_row = []
        for cell in range(len(row)):
            if row[cell] != 0:
                #the new row have the occupied blocks first
                new_row.append(row[cell])
        for empty in range(len(row) - len(new_row)):
            #the rest of the row is filled with empty block
            new_row.append(0)
        return new_row

    def merge_row(self, row):
        """This function merge the same numbers next to each other
        Paramters:
            :param row: a list that contains each item in the 4 blocks
        """
        found_pair = False
        new_row = []
        for cell in range(len(row)):
            if found_pair == True:
                #if there is a pair, add the sum of them to new_row
                #append 0 as a place holder before merging them
                new_row.append(0)
                new_row.append(2 * row[cell])
                #add the merge amount to the score
                self.score += 2 * row[cell]
                #set to False until find another pair
                found_pair = False
            else:
                if cell + 1 < len(row) and row[cell] == row[cell + 1]:
                    #if the blocks are not out of range and the next block equal to the current block, 
                    #a pair is found
                    found_pair = True
                else:
                    #at the last block, append the number in that block
                    new_row.append(row[cell])
        return new_row

    def draw(self):
        """this function draw the game board that contains the score and the game matrix
        """
        print(" SCORE: " + str(self.score))
        for row in range(self.height):
            self.draw_row_seperator()
            self.draw_cell_in_row(row)
        self.draw_row_seperator()
            
    def draw_row_seperator(self):
        """this function draw a separater of the game matrix
        """
        print("+———————" * (self.width) + "+")
    
    def draw_cell_in_row(self, row):
        """ this function draw the blocks in each row
        Paramters:
            :param row: a list that contains each item in the 4 blocks
        """
        row_str = ""
        for num in self.field[row]:
            if num == 0:
                row_str += "|       "
            else:
                #this format put the number at the center of the block
                row_str += "|{: ^7}".format(num)
        print(row_str+"|")

class Player:
    def __init__(self):
        """ the constructor method of the Player class
        """
        # there are 5 actions: move to one of four directions or exit the game
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT", "EXIT"]
        #use wasde to control the movement
        self.letter_codes = [char for char in "wsadeWSADE"]
        #match each letter code to the action: wW for up, aA for left, sS for down, dD for right, eE for exit
        self.actions_dict = dict(zip(self.letter_codes, self.actions * 2))
        self.gameboard = GameBoard()
    
    def get_action(self):
        """ this method get a user action and move or exit the game based on the action given 
        """
        correct_input = False
        while correct_input == False:
            #only make action when a valid input is given
            action_code = input("Please enter a correct action code then press ENTER. \n UP(w) DOWN(s) LEFT(a) RIGHT(d) EXIT(e) ")
            if action_code in self.letter_codes:
                correct_input = True
                if action_code in 'wsadWSAD':
                    #move to the given direction if movable
                    if self.gameboard.movable_in_direction(self.actions_dict[action_code]):
                        self.gameboard.move(self.actions_dict[action_code])
                    else:
                        #if not movable, let the player enter an action again
                        print("\nCannot move in the direction you just entered!\n")
                        correct_input = False
                else:
                    #clear the screen and exit the game
                    os.system('cls' if os.name == 'nt' else 'clear')
                    exit()

class Computer:
    def __init__(self):
        """The constructor method for Computer class
        """
        self.gameboard = GameBoard()
    
    def act(self):
        """ The computer always move based on a best strategy
        """
        self.gameboard.move(self.best_move())


    def best_move(self):
        """ This defines a best movement strategy for the computer player
        """
        potential_moves = self.get_potential_move()
        if len(potential_moves) == 1:
            #if there is only one potential move, move to that direction
            return potential_moves[0]
        else:
        #for each potential movement direction, the computer calculate the score earned
        #the direction earning the highest score is defined as the best direction to move 
            highest_score = 0
            best_direction = potential_moves[0]
            for i in range(len(potential_moves)):
                temp_gameboard = copy.deepcopy(self.gameboard)
                temp_gameboard.move(potential_moves[i])
                if temp_gameboard.score > highest_score:
                    highest_score = temp_gameboard.score
                    best_direction = potential_moves[i]
            return best_direction

    def get_potential_move(self):
        """This get all the potential moving direction
        """
        potential_moves = []
        for direction in ["LEFT", "RIGHT", "UP", "DOWN"]:
            #if it is movable to a direction, that direction is append to the potnetial_move list
            if self.gameboard.movable_in_direction(direction):
                potential_moves.append(direction)
        return potential_moves

    

def main():
    """This function run the game
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to the NEW 2048 game! \n\nInstructions:\nThe goal is to move cells and merge them to reach 2048!")
    print("You will also need to compete with a COMPUTER player.\nWhoever reaches 2048 first will win the game!")
    print("OR whoever cannot move anymore first will lose the game!")
    print("\nIf you and the computer reach 2048 at the same time,\nor cannot move at the same time,\nwhoever has the highest score wins.")
    print("\nYou can move cell by entering a singel action code and press ENTER.")
    print("Here are the action codes:")
    print("UP(w) DOWN(s) LEFT(a) RIGHT(d) EXIT(e)")
    state = "GAME"
    player = Player()
    computer = Computer()
    input("\nPress ENTER to continue.")
    while state == "GAME":
        #clear the previous game board before each round
        os.system('cls' if os.name == 'nt' else 'clear')
        #darw the game board for two players
        print("|===============================|")
        print("|      Computer Gameboard       |")
        computer.gameboard.draw()
        print("\n\n|===============================|")
        print("|        Player Gameboard       |")
        player.gameboard.draw()
        #check winning state after each movement
        if player.gameboard.check_win() == True and computer.gameboard.check_win() == False:
            state = "WIN"
            #if player reaches 2048 first, player win
            break
        elif computer.gameboard.check_loss() == True and player.gameboard.check_loss() == False:
            state = "WIN"
            #if computer ran out of move first, plater win
            break
        elif computer.gameboard.check_win() == True and player.gameboard.check_win() == False:
            state = "LOSS"
            #if computer reaches 2048 first, player lose
            break
        elif player.gameboard.check_loss() == True and computer.gameboard.check_loss() == False:
            state = "LOSS"
            #if player ran out of move first, player lose
            break
        elif player.gameboard.check_loss() == True and computer.gameboard.check_loss() == True:
            if computer.gameboard.score > player.gameboard.score:
                #if computer and player ran out of move at the same time, higher score wins
                state = "LOSS"
            else:
                state = "WIN"
            break
        elif player.gameboard.check_win() == True and computer.gameboard.check_win() == True:
            if computer.gameboard.score > player.gameboard.score:
                #if compiter and player reach 2048 at the same time, higher score wins
                state = "LOSS"
            else:
                state = "WIN"
            break
        #computer and player move
        computer.act()
        player.get_action()

    if state == "WIN":
        print("\nYou won!\n")
    elif state == "LOSS":
        print("\nYou lost...\n")

if __name__ == "__main__":
    main()