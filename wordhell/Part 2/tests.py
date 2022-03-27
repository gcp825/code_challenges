from wordhella import guess_barrage
import json

#############################################
# visual unit test
#############################################

answer =   'siege'
wordlist = ['liege','siege','hammy','eerie','chime','cuvee','wooze','beige','guile','crust','crepe']
guesses  = ['hammy','wooze','cuvee','eerie','liege']

print('#### Test 1: ####')

remaining_words = guess_barrage(answer,wordlist,guesses)
assert len(remaining_words) == 1
assert remaining_words[0] == 'siege'

#############################################
# verify against given example
#############################################

answer = 'piece'
wordlist = [word for word, _ in json.load(open('custom_wordlist.json', 'r')).items()]
guesses = ['eerie','about']

print('#### Test 2: ####')

remaining_words = guess_barrage(answer,wordlist,guesses)
assert len(remaining_words) == 10
assert 'piece' in remaining_words
