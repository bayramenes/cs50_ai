import sys

from crossword import *
from pprint import pprint
from copy import deepcopy




class queue:
    def __init__(self,items = []):
        self.items = items

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # go through each node  
        for variable in self.domains:
            # print(variable)
            # go through each word in the node's domain and make sure it is the right length
            for word in self.domains[variable].copy():

                if len(word) != variable.length:
                    self.domains[variable].remove(word)


            # print(self.domains[variable])




    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # initialize revised to false
        # and if we change anything we will turn it to True
        revised = False



        # first we want to check that there is an overlap between these two words
        overlap = self.crossword.overlaps[x, y]


        # if there is no overlap
        if overlap is None:
            # print("they don't overlap 🔴")
            return  revised
        
        # print(f"they overlap at {overlap} 🟢")


        # we are iterating over the copy so that we can remove items from the original list
        # to avoid errors
        for x_value in self.domains[x].copy():

            found = False
        
            # if there is no word in y such that the overlap has the same letter

            # we don't need copy since we are not going to modify it
            for y_value in self.domains[y]:

                # if there is a word that works
                if x_value[overlap[0]] == y_value[overlap[1]]:


                    # print(f"found a match for {x_value} and {y_value} 🟡")

                    found = True
                    break


            if not found:
                # remove that particular word from x's domain since there is no corresponding value for y
                self.domains[x].remove(x_value)
                revised = True


        # print(f"after revise {self.domains[x]} 🔵")
        # if revised :
        #     print("it was revised 👌")
        # else:
        #     print("it wasn't revised 👊")


        return revised
            
            

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # if arcs is None then initialize a list of all arcs
        if arcs is None:
            arcs = queue(list(self.crossword.overlaps.keys()))

        # continue until all arcs are done
        while not arcs.isEmpty():
            # get the first arc while removing it from the list of arcs
            (v1,v2) = arcs.dequeue()
            # print(f"checking {v1,v2}")

            if self.revise(v1,v2):
                # if the domain of v1 is empty then there is no solution
                if len(self.domains[v1]) == 0:
                    # print(f"{v1} domain is empty")
                    return False
                # if there is still a domain for v1 then we need to check if there is a connection between v1 and other nodes

                # go through each neighbour
                for neighbour_variable in self.crossword.neighbors(v1):
                    # add the arc to the list of arcs
                    arcs.enqueue((neighbour_variable,v1))


            # if nothing changed in v1 then we don't have to worry about anything
        
        # if we never return false meaning that after finishing all arcs there is no node that has an empty domain then we can 
        # be assured that arc consistency is made and we return True


        return True



    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # print("assignemt_complete:")
        # self.print(assignment)
        for variable in self.crossword.variables:
            # print(f"assignment_complete variable : {variable}")
            if variable not in assignment or assignment[variable] is None:
                return False
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for variable in assignment:
            # if the length of the word does not match the length of the variable
            # check for length
            if len(assignment[variable]) != variable.length:
                return False
            
            # check for uniqueness
            if len(set(assignment.values())) != len(assignment):
                return False
            
        # check for conflicts

        # for this we have to get overlaps
        # after that we have to check whether the words in the overlap do actually have the same letters at the intersection
        overlaps = self.crossword.overlaps
        for (v1,v2) in overlaps:
            # make sure that both variables have a value assigned to them
            if v1 not in assignment or v2 not in assignment:
                continue

            # if there is no overlap then we can skip this
            if overlaps[v1,v2] is None:
                continue

            # if the words do not have the same letters at the intersection then we can skip this
            if assignment[v1][overlaps[v1,v2][0]] != assignment[v2][overlaps[v1,v2][1]]:
                return False
            

        # if nothing goes wrong then return true
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domain = self.domains[var]

        # a list that will keep track of the results
        # then we will sort it
        result = []



        # go through each value in the domain
        for value in domain:
            ruled_out = 0
            # go through each neighbour of the node
            for neighbour in self.crossword.neighbors(var):
                if neighbour in assignment:
                    continue



                found = False
                # to check the number of values ruled out
                # we have to go through each value in the domain of the neighbour
                # and check whether the value overlaps with the value in the domain 
                # if so then we will check the overlapping characters
                # if not the same then we will count as a ruled out value
                var_index , neighbour_index = self.crossword.overlaps[var, neighbour]
                for neighbour_value in self.domains[neighbour]:
                    # if there is a value that still works then this isn't rules out
                    if value[var_index] == neighbour_value[neighbour_index]:
                        found = True
                        break

                if not found:
                    ruled_out += 1
            # after calculating all of the neighbors that will be rules out by this value add to the list
            result.append(value)

        # after getting all the values and their corresponding number of ruled out neighbors we will sort in ascending order
        result = sorted(result, key=lambda x: x[1])
        # then we will return the values in the sorted order
        return result

                
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # assigned values as a set
        assigned = set(assignment.keys())
        # print(f"select_unassigned_variable assigned : {assigned}")

        # get all unassigned variables
        unassigned = self.crossword.variables - assigned
        # print(f"select_unassigned_variable unassigned : {unassigned}")

        # if there are no unassigned variables then return None
        if len(unassigned) == 0:
            return None
        





        # initialize to be the first one
        best_variable = list(unassigned)[0]


        for unassigned_variable in unassigned:
            if len(self.domains[unassigned_variable]) < len(self.domains[best_variable]):
                best_variable = unassigned_variable
            # if there is a tie then choose according to degree
            elif len(self.domains[unassigned_variable]) == len(self.domains[best_variable]):
                degree_best = len(self.crossword.neighbors(best_variable))
                degree_unassigned = len(self.crossword.neighbors(unassigned_variable))
                if degree_best < degree_unassigned:
                    best_variable = unassigned_variable

            # if the number of words is already more then just go to the next variable
            else:
                continue




        return best_variable

            
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # if the assignment is complete then return it
        # self.print(assignment)
        # print(self.assignment_complete(assignment))
        if self.assignment_complete(assignment):
            return assignment
        
        # get the unassigned variable
        
        unassigned = self.select_unassigned_variable(assignment)

        # print(f"backtrack unassigned variable: {unassigned}")
        # get the ordred domain of the variable
        domain = self.order_domain_values(unassigned, assignment)
        # print(f"backtrack domain: {domain}")
        

        
        # for each value in the domain
        for value in domain:

            # create a new assignment
            new_assignment = assignment.copy()
            new_assignment[unassigned] = value

            # if the assignment is consistent then go to the next value
            if self.consistent(new_assignment):

                backup_domains = deepcopy(self.domains)

                inference = self.inference(new_assignment, unassigned)

                # there cannot be arc consistency when assigning this value to the variable
                if not inference:
                    self.domains = backup_domains
                    continue


                # before making a recursive call we can make use of inference in order to reduce the domain of the variable
                
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result

        # if the assignment is not complete then return None
        return None
    
    def inference(self,assignment,var):
        # change the domain of every variable that has been assigned a value to only include that particular value
        for assigned in assignment:
            self.domains[assigned] = {assignment[assigned]}
        

        inference_arcs = queue()
        for neighbor in self.crossword.neighbors(var):
            inference_arcs.enqueue((neighbor,var))
        
        enforced = self.ac3(arcs = inference_arcs)
        return enforced

    

    

        


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
