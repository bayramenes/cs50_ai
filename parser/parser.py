import nltk

import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""


# SP stands for sentence part
# sentence parts can be seperated by conjuctions that connects the different parts
# sentence parts should contain verb phrases at least alongside with noun phrases and adverbs
# noun phrases can contain nouns or some adjective or determiner before the noun
# COMP stands for compelemntary meaning that it is an extra word(s) that come after a verb and it can anything from noun to an adverb


# NOTE: i am no expert at english grammar so i might have some issues here
NONTERMINALS = """
S -> SP | SP Conj SP
SP -> NP VP | NP Adv VP | VP
NP -> N | NA N 
NA -> Det | Adj | NA NA
VP -> V | V COMP
COMP -> NP | P | Adv | COMP COMP | COMP COMP COMP

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")

        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # make sure that all the letters are lowercase
    sentence = sentence.lower()
    # get all the tokens
    tokens = nltk.word_tokenize(sentence)
    # go through each token and check if it contains any alphabetical character
    # if so then keep it if there are not alpahbetical characters at all then remove it
    for token in tokens:
        # check if there is any alphabetical letter in the token
        keep = any(c.isalpha() for c in token)
        if not keep:
            tokens.remove(token)
    

    return tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # initialize a noun phrase chunk list to return
    noun_phrase_chunk = []

    # we can go the hard route and write a recursive function where we read the whole tree trying to find every possible solutions
    # or we can use the nltk library api which has a function called subtree which will return a list of all of the subtrees of a given tree
    # provided it is a Tree object
    # so here is the plan:
    # we will go through each subtree and check its label if it is not NP then we will immediately skip else we have to check if it contains any
    # other NP subtree withing if none then add to the list


    # get all of the subtrees of the main tree

    for subtree in tree.subtrees():
        # check if the subtree is a NP subtree
        if subtree.label() == "NP":
            # check if the subtree contains any other NP subtree
            # any() return True if any of the elements are True
            # note that we have [1:] because .subtrees() return the all subtrees including the tree itself which creates a problem
            subtree_check = [subtree2.label() == "NP" for subtree2 in subtree.subtrees()][1:]
            if not any(subtree_check):
                # if none then add to the list
                noun_phrase_chunk.append(subtree)

    return noun_phrase_chunk


if __name__ == "__main__":
    main()
