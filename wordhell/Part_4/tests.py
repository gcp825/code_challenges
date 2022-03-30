from wordhell import filter_words, rank_solver, alphabetic, two_guesses_then_alphabetic

##########################################################
# Test filter_words with handcrafted test
##########################################################

answer =   'siege'
wordlist = ['liege','siege','hammy','eerie','chime','cuvee','wooze','beige','guile','crust','crepe']
guesses  = ['hammy','wooze','cuvee','eerie','liege']

print('#### Test 1: ####')

for guess in guesses:
    wordlist = filter_words(guess,answer,wordlist)
    print(guess,wordlist)

assert len(wordlist) == 1
assert wordlist[0] == 'siege'

##########################################################
# Test filter_words with eerie/about example
##########################################################

answer = 'piece'
wordlist = open('words.txt','r').read().split('\n')
guesses = ['eerie','about']

print('#### Test 2: ####')

for guess in guesses:
    wordlist = filter_words(guess,answer,wordlist)
    print(wordlist)
assert len(wordlist) == 10
assert 'piece' in wordlist

##########################################################
# Test rank_solver with simple alphabetic chooser function
##########################################################

print('#### Test 3: ####')

wordlist = open('words.txt','r').read().split('\n')
score = rank_solver(wordlist,alphabetic)
print(score)
assert score[0] == 9806 and score[1] == 75.74 and score[2] == -19325
     
##########################################################
# Test example two_guesses_then_alphabetic solver
##########################################################

print('#### Test 4: ####')

wordlist = open('words.txt','r').read().split('\n')
score = rank_solver(wordlist,two_guesses_then_alphabetic,('soare','input'))
print(score)
assert score[0] == 11291 and score[1] == 87.21 and score[2] == 1755

##########################################################
# Test two_guesses_then_alphabetic with better words
##########################################################

print('#### Test 5: ####')

wordlist = open('words.txt','r').read().split('\n')
score = rank_solver(wordlist,two_guesses_then_alphabetic,('suite','manor'))
print(score)
assert score[0] == 11315 and score[1] == 87.39 and score[2] == 2190