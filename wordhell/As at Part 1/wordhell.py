from collections import Counter

def get_result(guess,answer):

    guess, answer, colours  = (guess.upper(), answer.upper(), [])

    letters = list(zip(guess[:len(answer)],answer))[::-1]
    greyout = [g for g,x in Counter(guess).items() for a,y in Counter(answer).items() for z in range(x-y) if g == a and x > y]

    for guessed, actual in letters:

        if   guessed == actual:   colours += ['GREEN']
        elif guessed in greyout:  colours += ['GREY'];  greyout.remove(guessed)
        elif guessed in answer:   colours += ['YELLOW']
        else:                     colours += ['GREY']

    return colours[::-1]
    