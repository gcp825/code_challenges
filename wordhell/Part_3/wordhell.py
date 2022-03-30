from multiprocessing import Pool,cpu_count
from collections     import Counter
from functools       import lru_cache
from itertools       import repeat,chain
from time            import time

@lru_cache(maxsize=None)
def get_result(guess,answer):
 
    result = ''
    letters = list(zip(guess[:len(answer)],answer))[::-1]
    excess  = [g for g,x in Counter(guess).items() for a,y in Counter(answer).items() for z in range(x-y) if g == a and x > y]

    for guessed, actual in letters:

        if   guessed == actual:  result += 'g'                            
        elif guessed in excess:  result += 'x';  excess.remove(guessed)
        elif guessed in answer:  result += 'y'                 
        else:                    result += 'x'

    return result[::-1]


def filter_words(guess,answer,wordlist):

#   the remaining words will be those that produce the same match pattern (colours) as the actual answer when compared to the same guess

    match_pattern = get_result(guess,answer)

    return tuple([word for word in wordlist if get_result(guess,word) == match_pattern])


def rank_solver(wordlist,solver_func):

    collated_results = []
    processes        = cpu_count()
    wordlist_chunks  = [wordlist[i::processes] for i in range(processes)]
    start_time       = time()

    with Pool(processes) as pool:
        collated_results += pool.starmap(solver_process,
                                         zip(wordlist_chunks,repeat(wordlist),repeat(solver_func)))

    totals   = [sum(x) for x in zip(*[(1 if score >= 0 else 0, 1, score) for answer, score in chain(*collated_results)])]
    duration = round(time()-start_time,2)
        
    return totals[0], round((totals[0]/totals[1])*100,2), totals[2], duration


def solver_process(answer_group,wordlist,solver_func):

    scores = dict()

    for answer in answer_group:

        words = tuple(wordlist)

        for guess in range(6):
            suggestion = solver_func(words)
            if suggestion == answer:
                break
            else:
                words = filter_words(suggestion,answer,words)
                
        scores[answer] = 5-guess if suggestion == answer else -10

    return list(scores.items())


# Solver functions...

def alphabetic(words): 
    
    return words[0]
