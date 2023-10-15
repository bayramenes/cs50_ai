import csv
import itertools
import sys
from pprint import pprint




# probabilities of having a certain number of genes given the parent genes
# for example if the mother has 2 genes and the father has 1 then the probability is PARENT_PROBS[2][1]
# in general it is PARENT_PROBS[mother][father]
PARENT_PROBS=[
        [1,0,0], [0.5,0.5,0], [0,1,0],
        [0.5,0.5,0], [0.25,0.5,0.25], [0,0.5,0.5],
        [0,1,0], [0,0.5,0.5], [0,0,1]
    ]


PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # starting from one_gene we will go through all the people 
    # 1. check whether they have parents or not
    # if so then we will calculate the conditional probability that they have one copy of the gene
    # 2. if they don't have parents then we will calculate the unconditional probability from the PROBS dictionary that they have one copy of the gene
    # we will do the same for two genes
    # lastly we will calculate the probability of having no genes for the people that aren't in both of the dictionaries
    # then we will calculate the probability of having a trait which is a conditional probability that depends on the probability of the number of genes that they have though the tricky part here is to take mutation into account



    # note that after i implemented the logic a certain way that i thought would be more effecient i realized that there are better ways
    # but if it ain't broken don't fix it so i will not be changing it



    probabilities = {
        person:{
            "gene": 0,
            "give": 0,
        }
        for person in people
    }


    # for two_gene_person in two_genes:
    #     # check if the person has a parent or not

    #     # if doesn't have a parent meaning is the top of the bayesian network
    #     if people[two_gene_person]["mother"] is None:
    #         probabilities[two_gene_person]["gene"] = PROBS["gene"][2]

    #     else:

    #         # if they have parents then there different combinations of parents of which that can occur
    #         # if the person has both parents with two copies of the gene
    #         # if the person has one parent with two copies of the gene and the other with one copy of the gene
    #         # if any of the parents has no copy of the gene then it is 
    #         probabilities[two_gene_person]["gene"] = PROBS["gene"][2] * 

    # for one_gene_person in one_gene:
    #     # check if the person has a parent or not

    #     # if doesn't have a parent meaning is the top of the bayesian network
    #     if people[one_gene_person]["mother"] is None:
    #         probabilities[one_gene_person]["gene"] = PROBS["gene"][1]

    #     # if has a parent then we will calculate the conditional probability that they have one copy of the gene
    #     else:
    #         pass

    parents = get_parents(people)
    # get the parents because we will need the their probabilities for the children
    for parent in parents:
        # determine what we need to calculate for the parent
        if parent in one_gene:
            # calculate the probability of having one copy of the gene
            probabilities[parent]["gene"] = PROBS["gene"][1]
            probabilities[parent]["give"] = 0.5
            if parent in have_trait:
                probabilities[parent]["gene"] *=  PROBS["trait"][1][True]
            else:
                probabilities[parent]["gene"] *=  PROBS["trait"][1][False]


        elif parent in two_genes:
            # calculate the probability of having two copies of the gene
            probabilities[parent]["gene"] = PROBS["gene"][2]
            probabilities[parent]["give"] = 1 - PROBS["mutation"]
            if parent in have_trait:
                probabilities[parent]["gene"] *=  PROBS["trait"][2][True]
            else:
                probabilities[parent]["gene"] *=  PROBS["trait"][2][False]
        else:
            probabilities[parent]["gene"] = PROBS["gene"][0]
            probabilities[parent]["give"] = PROBS["mutation"]
            if parent in have_trait:
                probabilities[parent]["gene"] *=  PROBS["trait"][0][True]
            else:
                probabilities[parent]["gene"] *=  PROBS["trait"][0][False]




    for one_gene_person in one_gene:
        if people[one_gene_person]["mother"] is not None:
            father = people[one_gene_person]["father"]
            mother = people[one_gene_person]["mother"]
            
            # we want to calculate the probability of only having 1 gene 

            # first case is if father doesn't give but mother gives

            p = probabilities[mother]["give"] * (1 - probabilities[father]["give"])

            # second case is if the father gives but the mother doesn't

            p += probabilities[father]["give"] * (1 - probabilities[mother]["give"])
            

            # check the probability of having trait
            if one_gene_person in have_trait:
                p *= PROBS["trait"][1][True]
            else:
                p *= PROBS["trait"][1][False]

            

            # lastly we add this probability to the probabilities dictionary
            probabilities[one_gene_person]["gene"] = p

    for two_gene_person in two_genes:
            if people[two_gene_person]["mother"] is not None:
                father = people[two_gene_person]["father"]
                mother = people[two_gene_person]["mother"]
                

                # we want to calculate the probability of having 2 genes
                # this is only the case if both parents give
                p = probabilities[mother]["give"] * probabilities[father]["give"]
                            # check the probability of having trait
                if two_gene_person in have_trait:
                    p *= PROBS["trait"][2][True]
                else:
                    p *= PROBS["trait"][2][False]

                

                # add this probability to the probabilities dictionary
                probabilities[two_gene_person]["gene"] = p
    

    for no_gene_person in (set(people.keys()) - one_gene - two_genes):
        if people[no_gene_person]["mother"] is not None:
            father = people[no_gene_person]["father"]
            mother = people[no_gene_person]["mother"]
            

            # we want to calculate the probability of not having any genes

            # this is only the case if both parents don't give
            p = (1 - probabilities[mother]["give"]) * (1 - probabilities[father]["give"])
            # check the probability of having trait
            if no_gene_person in have_trait:
                p *= PROBS["trait"][0][True]
            else:
                p *= PROBS["trait"][0][False]

            # add this probability to the probabilities dictionary
            probabilities[no_gene_person]["gene"] = p

    # after calculating this we have to calculate the probability of having a trait or not based on the probability of the number of genes

    # first we are going to calculate the probability of having a trait given the number of genes
    
    # initialize the probabilty to 1
    probability = 1
    for person in people:
        probability *= probabilities[person]["gene"]

    return probability



def get_parents(people):
    """
    returns a list of the names of the parents for a particular family
    """
    parents = []
    for person in people:
        if people[person]["mother"] not in parents and people[person]["mother"] is not None:
            parents.append(people[person]["mother"])

        if people[person]["father"] not in parents and people[person]["father"] is not None:
            parents.append(people[person]["father"])

    return parents




def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # normalize the gene distribution
        gene_sum = sum(list(probabilities[person]["gene"].values()))
        normalization_factor = 1 / gene_sum
        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] *= normalization_factor

        # normalize the trait distribution
        trait_sum = sum(list(probabilities[person]["trait"].values()))
        normalization_factor = 1 / trait_sum
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] *= normalization_factor


if __name__ == "__main__":
    main()
