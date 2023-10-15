import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # first case is if the count is equal to the length of the set of cells
        # this means that all of the cells are mines
        if len(self.cells) == self.count:
            return self.cells
        # second is if the count is 0 this means that none are mines
        elif self.count == 0:
            return set()
        # otherwise we don't know
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # first case is if the count is equal to the length of the set of cells
        # this means that all of the cells are mines
        if len(self.cells) == self.count:
            return set()
        # second is if the count is 0 this means that none are mines
        elif self.count == 0:
            return self.cells
        # otherwise  we don't know
        return set()
    

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            # update the mine count since we found a new mine
            self.count -= 1
            # remove this cell from the sentence since it is a mine
            self.cells.remove(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            # remove this cell from the sentence since it is safe
            self.cells.remove(cell)
            # we don't need to update count since this is a safe cell and not a mine
            # and our count is the number of mines in the sentence


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """

        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # mark as a move
        self.moves_made.add(cell)

        # mark as safe
        self.mark_safe(cell)
        # create a new sentence based on the cell and the count

        # we will loop over the 3x3 surrounding the move and check
        # if the cell isn't played 
        # if yes then we will check if it is a mine or not
        # and build our sentence accordingly 

        neighbours = []
        for row in range(3):
            for col in range(3):
                # check if the cell is in the bounds of the board
                if 0 <= cell[0] + row - 1 < self.height and 0 <= cell[1] + col - 1 < self.width:

                    # if this is a move that hasn't been made yet
                    # if so then we want to add it to the sentence
                    if (cell[0] + row - 1, cell[1] + col - 1) not in self.moves_made:

                        # if the cell is known to be a mine then we don't want to add it to the sentence
                        # but instead we want to subtract 1 from the count since we know that there is a mine
                        if (cell[0] + row - 1, cell[1] + col - 1) in self.mines:
                            count -= 1
                        elif (cell[0] + row - 1, cell[1] + col - 1) in self.safes:
                            continue
                        else:
                            # add the cell to the sentence
                            neighbours.append((cell[0] + row - 1, cell[1] + col - 1))


        # create a new sentence with the updated neighbours and count
        new_sentence = Sentence(neighbours, count)

        # add the new sentence to the knowledge base
        self.knowledge.append(new_sentence)


        # this is a piece of code that will continue updating the knowledge base
        # until we can't update it anymore without any move

        # note taht process_knowledge return true if something was updated false otherwise
        while True:
            updated = self.process_knowledge()

            if not updated:
                break
            else:
                continue








    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # if there are some cells that are known to be safe but hasn't been played yet
        if len(self.safes - self.moves_made) != 0:
            new_move = list(self.safes - self.moves_made)[0]
            self.moves_made.add(new_move)
            return new_move
        

        # if all of the safe moves that are known 
        else:
            return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) not in self.moves_made and (row, col) not in self.mines:
                    return (row, col)
        return None


    # the idea of this function is to check the knowledge base and see if we can conclude any new sentences or 
    # mark some cells as mines or safes.
    # i think that the best is to keep track of whether we have updated our knowledge base or not
    # and if we have updated our knowledge base then we want to return True else we return False
    # this is so that we can continue updating our knowledge base to the point we can't update it anymore without any move
    def process_knowledge(self):
        """
        Processes the knowledge in the knowledge base.
        """

        is_updated = False
        


        # remove any empty sets from the knowledge base
        for sentence in self.knowledge:
            if sentence.cells == set():
                self.knowledge.remove(sentence)


        # now we want to go over our knowledge base and check if we can infer anything


        # first we are going to check if any sentence is a subset of another sentence because this way we can produce 
        # a new sentence that might potentially be useful

        for sentence1 in self.knowledge.copy():
            for sentence2 in self.knowledge.copy():


                # if sentence1 is a subset of sentence2 but not the same sentence
                # we want to produce a new sentence sentence2 - sentence1 = count2 - count1
                if sentence1 != sentence2 and sentence1.cells.issubset(sentence2.cells):


                    # then sentence1 is a subset of sentence2
                    new_cells = sentence2.cells - sentence1.cells
                    new_count = sentence2.count - sentence1.count
                    new_sentence = Sentence(new_cells, new_count)
                    # we have to remove the sentence2 since it contains sentence1 and we don't need anymore
                    self.knowledge.remove(sentence2)
                    self.knowledge.append(new_sentence)
                    is_updated = True







        for sentence in self.knowledge:
            # check if we have any known mines that aren't added to the list of mines yet
            mines = sentence.known_mines()
            # go through each mine
            # and check whether it is a known mine or not
            # if not then we mark it as a mine
            for mine in mines.copy():
                if mine not in self.mines:
                    self.mark_mine(mine)
                    is_updated = True
            
            # we will do the smae process but this time for safes

            safes = sentence.known_safes()
            for safe in safes.copy():
                if safe not in self.safes:
                    self.mark_safe(safe)
                    is_updated = True
        
        return is_updated
            
            


