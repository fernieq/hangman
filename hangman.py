path = 'hw2_word_counts_05.txt'
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
for c in alphabet:
	c = c.upper();

def getValue(item):
	return item[1]

def isGameboardValid(gameboard, word):
	for i in range(5):
		if(word[i] != gameboard[i] and gameboard[i] != ''):
			return False
	return True

def couldBeInWord(gameboard, word, c):
	for i in range(5):
		if(gameboard[i] == ''):
			if(word[i] == c):
				return 1.0

	return 0.0

def checkWord(gameboard, word, incorrect):
	for i in range(5):
		if(gameboard[i] != ''):
			if(gameboard[i] != word[i]):
				return 0.0

	for c in incorrect:
		if(c in word):
			return 0.0

	return 1.0

with open(path) as f:
	content = f.readlines()

#2.3.a
'''
['BOSAK', 6]
['CAIXA', 6]
['MAPCO', 6]
['OTTIS', 6]
['TROUP', 6]
['CCAIR', 7]
['CLEFT', 7]
['FABRI', 7]
['FOAMY', 7]
['NIAID', 7]
['OTHER', 106052]
['FIFTY', 106869]
['FIRST', 109957]
['AFTER', 110102]
['WHICH', 142146]
['THEIR', 145434]
['ABOUT', 157448]
['WOULD', 159875]
['EIGHT', 165764]
['SEVEN', 178842]

These results make a lot of sense since the least common 5 are barely ever used,
with the only word I know of that lot being 'troup' and the most common 5 are probably
used everday within a sentence
'''
def partA():
	pairs = [[d.split(' ')[0], int(d.split(' ')[1])] for d in content];
	pairs = sorted(pairs, key=getValue)
	for i in range(10):
		print (pairs[i])

	for i in range(10):
		print (pairs[len(pairs) - 11 + i])

#2.3.b
'''
game = ['', '', '', '', ''];
incorrect = [];
mostLikely = ['E', 0.5394172389647948]

game = ['', '', '', '', ''];
incorrect = ['E', 'O']
mostLikely = ['I', 0.6365554141009618]

game = ['Q', '', '', '', '']
incorrect = []
mostLikely = ['U', 0.9866727159303582]

game = ['Q', '', '', '', '']
incorrect = ['U']
mostLikely = ['A', 0.9999999999999999]

game = ['', '', 'Z', 'E', '']
incorrect = ['A', 'D', 'I', 'R']
mostLikely = ['O', 0.8803418803418803]
'''

#gameboard is a list [ 'a', 'b', '', '', 'e' ] for example word 'abode'
#incorrect is a set {u,t,s} of letters already guessed
def partB(gameboard, incorrect):
	pairs = [[d.split(' ')[0], int(d.split(' ')[1])] for d in content];
	#validWords = [word for word in pairs if isGameboardValid(gameboard, word[0])]

	countTotal = 0;
	for word in pairs:
		countTotal += word[1]


	probabilities = [];

	for c in alphabet:
		if(c not in incorrect and c not in gameboard):
			denominator = 0.0;
			for word in pairs:
				denominator += (word[1] / countTotal) * checkWord(gameboard, word[0], incorrect)

			probability = 0.0;
			for word in pairs:
				probability += couldBeInWord(gameboard, word[0], c) * checkWord(gameboard, word[0], incorrect) * (word[1] / countTotal) / denominator

			probabilities.append([c, probability])
		else:
			probabilities.append([c, 0.0])

	probabilities = sorted(probabilities, key=getValue, reverse=True)
	print(probabilities[0])


partA()

game = ['', '', '', '', ''];
incorrect = [];
partB(game, incorrect);

incorrect = ['E', 'O']
partB(game, incorrect)

game = ['Q', '', '', '', '']
incorrect = []
partB(game, incorrect)

game = ['Q', '', '', '', '']
incorrect = ['U']
partB(game, incorrect)

game = ['', '', 'Z', 'E', '']
incorrect = ['A', 'D', 'I', 'R']
partB(game, incorrect)
