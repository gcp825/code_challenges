from collections import Counter
from string import ascii_lowercase
import re

#  Given a guess and the answer, return a list of colours for each letter of the guess + a colourised display version of the guess

def get_result(guess,answer):
 
    colour_codes = {'🟩':'\033[32m','🟨':'\033[33m','⬛':'\033[0m','⬜':'\033[0m'}

    answer, guess, result = (answer.lower(), guess.lower(), [])

    letters = list(zip(guess[:len(answer)],answer))[::-1]
    excess  = [g for g,x in Counter(guess).items() for a,y in Counter(answer).items() for z in range(x-y) if g == a and x > y]

    for guessed, actual in letters:

        if   guessed == actual:  result += ['🟩']                            
        elif guessed in excess:  result += ['⬜'];  excess.remove(guessed)
        elif guessed in answer:  result += ['🟨']                 
        else:                    result += ['⬛']

    colours = result[::-1]
    display_guess = ''.join([colour_codes[col] + guess[i] for i,col in enumerate(colours)]) + colour_codes['⬛']

    return guess, colours, display_guess


#  Coroutine, initialised with a wordlist, that narrows down the potential answers when the result from the above function is sent to it

def solver(wordlist):

    minimum, exact, length = (dict(), dict(), len(wordlist[0]))

    prospects = wordlist
    possible  = [list(ascii_lowercase)] * length
  
    while len(prospects) > 1:

        #  receive the latest guess & colours (colours) for that guess via send()  

        guess, colours, _ = yield                                                                                         
        letters = list(zip(colours,range(length),guess))

        #  update the list of possible letters remaining for each character of the answer

        for colour, i, letter in letters :                                

            if   colour == '🟩':  possible[i] = [letter]
            elif colour == '⬛':  possible    = [[p for p in possible[x] if p != letter] for x in range(length)]
            else:                 possible[i] = [p for p in possible[i] if p != letter]                      

        #  an excess of a particular letter in the guess allows us to record the exact number of occurences of that letter in the answer
        #  also remove that letter from the dict of minimum values should it exist there

        for _, _, letter in [x for x in letters if x[0] == '⬜']:    

            exact[letter] = sum([1 for colour, _, l in letters if colour in ('🟩','🟨') and l == letter])
            minimum.pop(letter,None)

        #  where we don't know exactly how many occurences of a letter are in the answer, record the minimum based on what we do know
        #  only update the dict if the minimum has increased

        for letter, ct in Counter([letter for colour,_,letter in letters if colour in ('🟩','🟨') and letter not in exact]).items():

            if ct > minimum.get(letter,0):
                minimum[letter] = ct

        #  Filter the list of possible answers based on possible letters for each position and known/minimum letter frequencies

        regex = ''.join(['[' + ''.join(p) + ']' for p in possible])
        prospects = [word for word in prospects if re.match(regex,word)
                                                and sum([1 for letter,ct in exact.items()   if word.count(letter) != ct]) == 0
                                                and sum([1 for letter,ct in minimum.items() if word.count(letter)  < ct]) == 0]

        yield prospects 


#  Function to initialise the solver coroutine and spam it with a series of guesses

def guess_barrage(answer,wordlist,guesses):

    game = solver(wordlist)

    i = 0
    for _ in game:
        result = get_result(guesses[i],answer)
        possible_answers = game.send(result)
        print(result[2],possible_answers)
        i += 1
        if i >= len(guesses): break

    return possible_answers 
