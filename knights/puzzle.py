from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")





# Puzzle 0
# A says "I am both a knight and a knave."


# this puzzle's statements
AStatement = And(AKnight, AKnave)

knowledge0 = And(


    # these are some general rules for the game 
 
    # we also know that a character can be either a knight or a knave not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # we also know that a character can be either a knight or a knave not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # we also know that a character can be either a knight or a knave not both
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),




    # we know that if he is knight this implies that what he tells is the truth
    Implication(AKnight, AStatement),
    # we also know that if he is a knave then this implies that what he tells is a lie
    Implication(AKnave, Not(AStatement)),
)



# Puzzle 1
# A says "We are both knaves."
# B says nothing.


# this puzzles statements
AStatement = And(AKnave, BKnave)

knowledge1 = And(

    # these are some general rules for the game 
 
    # we know that a character can be either a knight or a knave not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # we know that a character can be either a knight or a knave not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # we know that a character can be either a knight or a knave not both
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),




    # we know that if he is knight this implies that what he tells is the truth
    Implication(AKnight, AStatement),
    # we also know that if he is a knave then this implies that what he tells is a lie
    Implication(AKnave, Not(AStatement)),

)




# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."


# this puzzles statements
AStatement = Or(
        And(AKnight, BKnight),
        And(AKnave, BKnave),
    )

BStatement = Or(
    And(AKnight, BKnave),
    And(AKnave, BKnight),
)

knowledge2 = And(
    
    # these are some general rules for the game 
 
    # we know that a character can be either a knight or a knave not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # we know that a character can be either a knight or a knave not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # we know that a character can be either a knight or a knave not both
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),


    Implication(AKnight, AStatement),
    Implication(AKnave, Not(AStatement)),
    Implication(BKnight, BStatement),
    Implication(BKnave, Not(BStatement)),
)



# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."



# this puzzles statements
AStatement = Or(AKnight, AKnave)

BStatement = And(
        CKnave,
        And(AStatement, AKnave)
    )

CStatement = AKnight


knowledge3 = And(


    # these are some general rules for the game 
 
    # we know that a character can be either a knight or a knave not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # we know that a character can be either a knight or a knave not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # we know that a character can be either a knight or a knave not both
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),



    Implication(AKnight, AStatement),
    Implication(AKnave, Not(AStatement)),
    Implication(BKnight, BStatement),
    Implication(BKnave, Not(BStatement)),
    Implication(CKnight, CStatement),
    Implication(CKnave, Not(CStatement)),

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
