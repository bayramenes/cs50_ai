import os
import random
import re
import sys
import copy
from pprint import pprint
DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages



def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # first we have to check whether the page has any links 
    # if the page doesn't have any links then we will return an equal probability for all pages
    distribution = {}

    if corpus[page] == set():
        for d_page in corpus:
            distribution[d_page] = 1/len(corpus)
    # if there are some links that the page has then we will have to calculate those new probabilities
    else:

        # first we will calculate the probability of going to any page in the corpus including the
        # one we are in right now but all multiplied by the (1 - damping_factor) constant

        random_probability = (1 - damping_factor) / len(corpus)
        for d_page in corpus:
            distribution[d_page] = random_probability

        # how many links does the page have?
        link_count   = len(corpus[page])

        # second lets calculate the probabiltiy of going to pages that are linked to this page
        # multiplied by the damping factor
        for linked_page in corpus[page]:
            # divide by the total number
            distribution[linked_page] += damping_factor * ( 1 / link_count  )



    return distribution

        


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    # initialize the pagerank dictionary with all the pages in the corpus
    for page in corpus:
        pagerank[page] = 0


    # choose a starting sample at random

    sample = random.choices(list(corpus.keys()))[0]
    # make n samples
    for sample_index in range(n):
        pagerank[sample] += 1/n
        # get the transition model for the sample
        model = transition_model(corpus, sample, damping_factor)
        # choose a new sample based on the model
        sample = random.choices(list(model.keys()), weights=list(model.values()))[0]

    return pagerank

    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # first we will initialize the pagerank dictionary with all the pages in the corpus
    # each page will have a value of 1/n at the start
    # n being the number of pages in the corpus
    pagerank = {}
    for page in corpus:
        pagerank[page] = 1/len(corpus)


    # the random contant that will be added on each new calculation
    # this is to ensure that we aren't stuck on a page that is not connected to any other pages

    random_probability = (1 - damping_factor) / len(corpus)
    
    
    while True:
        did_converge  = True
        # make a copy of the current page rank scores
        current_pagerank = copy.deepcopy(pagerank)



        for page in corpus:
            
            # add the random constant
            pagerank[page] = random_probability

            # check if the page has any links
            # if none then we will calculate as if it has a link to every page in the corpus including itself
            if corpus[page] == set():
                for linked_page in corpus:
                    pagerank[page] += damping_factor * ( current_pagerank[linked_page] / len(corpus) )

                # check for the difference between the current pagerank score and the newly calculated pagerank score
                # if the difference is greater than 0.001 then we will set the did_converge variable to false meaning
                # we haven't converged yet hence we will continue this process until convergence
                if abs(pagerank[page] - current_pagerank[page]) > 0.001:
                    did_converge = False
            else:

                # this is the same as the sigma notation
                # we are going to go through each page that links to the current page
                # for each linked page add it to the pagerank value after damping it with a factor

                for linked_page in pointing_pages(corpus, page):

                    pagerank[page] += damping_factor * ( current_pagerank[linked_page] / len(corpus[linked_page]) )


                # check for the difference between the current pagerank score and the newly calculated pagerank score
                # if the difference is greater than 0.001 then we will set the did_converge variable to false meaning
                # we haven't converged yet hence we will continue this process until convergence
                if abs(pagerank[page] - current_pagerank[page]) > 0.001:
                    did_converge = False

        if did_converge:
            break

    return pagerank




def pointing_pages(corpus, page):
    """
    Return a list of pages pointing to the given page.
    """
    pointing_pages = []
    for page_name, links in corpus.items():
        if page in links:
            pointing_pages.append(page_name)

    return pointing_pages




if __name__ == "__main__":
    main()
