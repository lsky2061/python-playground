import itertools
import math


def get_lowercase_letters():
    return list(map(chr, range(97, 123)))


def contains_all_letters(word_list, required_letters):
    tmp = required_letters.copy()
    for word in word_list:
        for letter in word:
            # print("Trying letter:", letter)
            # print(word.find(letter))
            if tmp.count(letter) > 0: tmp.remove(letter)

        if len(tmp) == 0:
            return True
        else:
            return False


def check_for_solutions(combination_list, required_letters):
    solutions = []
    for subset in combination_list:
        tmp = required_letters.copy()
        # print(subset)
        for word in subset:
            for letter in word:
                # print("Trying letter:", letter)
                # print(word.find(letter))
                if tmp.count(letter) > 0: tmp.remove(letter)

            if len(tmp) == 0:
                print("Solution:", subset)
                solved = True
                solutions.append(subset)
    return solutions


def longer_solutions(previous_list, valid_words):
    out_list = []
    for start_list in previous_list:
        # print('Checking for ',start_list)
        for add_word in valid_words:
            last_letter = start_list[-1][-1]
            first_letter = add_word[0]
            last_word = start_list[-1]
            if last_letter == first_letter and last_word != add_word:
                tmp = start_list.copy()
                tmp.append(add_word)
                out_list.append(tmp)
    return out_list


def add_unique_letters(previous_list, valid_words, cutoff=1e9):
    out_list = []
    n_tests = len(previous_list) * len(valid_words)
    print(f'Expecting {len(previous_list)} x {len(valid_words)} = {n_tests} combinations to be tested.')
    count = 0
    for start_list in previous_list:
        for add_word in valid_words:
            frac = count / n_tests
            perc = frac * 100
            if (count % 1e6 == 0):
                print(f'Testing combination {count} of {n_tests}. {perc:.2f}% complete')
            overlap = 0
            for prev_word in start_list:
                overlap += len(set(prev_word) & set(add_word))
            count += 1
            if overlap == 0:
                #out_list.append([start_list[0], start_list[1], add_word])
                tmp = start_list.copy()
                tmp.append(add_word)
                out_list.append(tmp)
                #print('Appended: ',list_3[-1])
            if count > cutoff: break

    return out_list


def word_clean_length(min_length):
    with open("/usr/share/dict/words") as f:
        words = f.read().splitlines()

    #Remove words with apostrophies
    #https://stackoverflow.com/questions/12666897/removing-an-item-from-list-matching-a-substring
    valid_words = [x for x in words if x.isalpha()]
    valid_words = [x for x in valid_words if len(x) >= min_length]

    cap_letters = list(map(chr, range(65, 91)))

    for cap in cap_letters:
        valid_words = [x for x in valid_words if x.find(cap) == -1]

    #Remove accents and diacritical marks
    for word in valid_words:
        for letter in word:
            a = ord(letter)
            if a <97 or a >123 and valid_words.count(word) > 0:
                valid_words.remove(word)

    return valid_words


def letterboxed():
    valid_words = word_clean_length(3)

    #https://stackoverflow.com/questions/16060899/alphabet-range-in-python
    letters = list(map(chr, range(97, 123)))

    sides = []
    #Get box sides from user
    for i in range(1, 5):
        good_input = False
        while not good_input:
            tmp = input(f'Enter letters for side {i}: ')
            if len(tmp) == 3 and tmp.isalpha():
                good_input = True
                sides.append(tmp)
            else:
                print("Please enter exactly 3 letters for this side")
    print('Sides: ', sides)
    #sides = [['t','s','h'],['o','i','j'],['u','c','n'],['p','b','e']]
    # Remove all words with letters not on the box
    forbidden_letters = letters.copy()
    required_letters = []
    for side in sides:
        for letter in side:
            forbidden_letters.remove(letter)
            required_letters.append(letter)

    print('Letters not in the box:', forbidden_letters)
    print('Letters in the box:', required_letters)
    for fl in forbidden_letters:
        valid_words = [x for x in valid_words if x.find(fl) == -1]

    # Remove all words with repeated letters (e.g. all, letters)
    forbidden_pairs = []

    for letter in letters:
        t = letter + letter
        forbidden_pairs.append(t)

    #Create list of "forbidden pairs" (any letters that are both on the same side of the box
    for side in sides:
        [forbidden_pairs.append(x + y) for x in side for y in side]

    #Remove all words with a forbidden pair
    print('The following pairs of letters are NOT allowed:', forbidden_pairs)
    for fp in forbidden_pairs:
        valid_words = [x for x in valid_words if x.find(fp) == -1]

    #Remove words with capital letters (eliminate proper nouns and acronyms)

    valid_words = sorted(valid_words, key=len, reverse=True)
    print('We have a total of', len(valid_words), 'possible valid words.')
    print(valid_words)
    solutions = []
    solved = False
    num_words = 1
    perm_words = [[], [], [], [], []]
    while not solved:
        combination_list = []
        if num_words == 1:
            combination_list = valid_words.copy()
            if len(combination_list[0]) < 12:
                print("No single word solution. Longest word is", len(combination_list[0]), "letters long.")
                print(combination_list[0])
                solved = False
            else:
                for word in combination_list:
                    tmp = required_letters.copy()
                    if len(word) >= 12:
                        #print(word)
                        for letter in word:
                            if tmp.count(letter) > 0: tmp.remove(letter)

                        if len(tmp) == 0:
                            solved == True
                            print("Single word solution:", word)
                if not solved: print("No single word solution found.")

        if num_words > 1:
            print(f'Looking for {num_words} word solutions.')
            #gather all possible permutations of valid words
            perms = itertools.permutations(valid_words, num_words)
            #Lets try to create the permutations more judiciously
            if num_words == 2:
                for start_word in valid_words:
                    for add_word in valid_words:
                        if start_word[-1] == add_word[0] and start_word != add_word:
                            perm_words[2].append([start_word, add_word])
                #print('2 word combos:', perm_words[2])

            if num_words > 4:
                perm_words.append([])
            if num_words > 2:
                perm_words[num_words] = longer_solutions(perm_words[num_words - 1], valid_words)

            #The number of permutations is n!/(n-r)! where n = len(valid_words) and r = num_words
            n_valid_words = len(valid_words)
            #n_perms = math.factorial(n_valid_words)/math.factorial(n_valid_words - num_words)
            n_perms = len(perm_words[num_words])

            count = 0
            for pw in perm_words[num_words]:
                count += 1
                if (count % 10000000 == 0):
                    print('Checking permutation #', count, 'of', n_perms, 'for', num_words, 'words. ',
                          (count / n_perms) * 100,
                          '% complete.')
                #print(type(pw))
                #Check if the last letter of each word is the first letter of the next word
                #I think this is redundant now

                tmp = []
                j = 0
                while j < num_words:
                    tmp.append(pw[j])
                    j = j + 1
                combination_list.append(tmp)
                #print('Valid combination:', tmp)
        solutions = check_for_solutions(combination_list, required_letters)

        if len(solutions) > 0: solved = True
        num_words += 1


#print(solutions)

def blossom_score(word, yellow_letter,sb=False):
    letter_score = 0
    yellow_bonus = 5
    pangram_bonus = 7

    n_letters = len(word)
    if n_letters == 4:
        letter_score = 2
    elif n_letters == 5:
        letter_score = 4
    elif n_letters == 6:
        letter_score = 6
    elif n_letters == 7:
        letter_score = 12
    else:
        letter_score = 12 + 3 * (n_letters - 7)

    if sb: #We are playing Spelling Bee
        if n_letters == 4:
            letter_score = 1
        elif n_letters >= 4:
            letter_score = n_letters


    yellow_bonus = 0
    if not sb:
        y = word.count(yellow_letter)
        #print('found',y,'yellow letters')
        yellow_bonus = 5 * y

    #print('letter score = ',letter_score)
    # print('yellow bonus = ', yellow_bonus)
    score = letter_score + yellow_bonus
    #pangram bonus
    #https://www.geeksforgeeks.org/count-the-number-of-unique-characters-in-a-string-in-python/
    if len(set(word)) == 7:
        print('pangram bonus!')
        score = score + 7

    #print('total score = ', score)
    return score



def blossom(sb=False):
    letters = input('What are the seven letters?  ')
    central = input('What is the central letter?  ')
    valid_words = word_clean_length(4)

    #Require central letter
    valid_words = [x for x in valid_words if x.find(central) >= 0]
    forbidden_letters = list(map(chr, range(97, 123)))
    required_letters = letters
    for letter in letters:
        forbidden_letters.remove(letter)

    for fl in forbidden_letters:
        valid_words = [x for x in valid_words if x.find(fl) == -1]

    print('We have', len(valid_words), 'valid words:', valid_words)
    used_words = []

    range_max = 12
    if(sb): range_max = len(valid_words)

    for round in range(1, range_max + 1):
        valid = False
        yellow = 'z'
        if not sb:
            yellow = input(f'For this round: {round}, what is the yellow petal?  ')

        while not valid:
            score = 0
            max_score = 0
            max_word = ''

            for word in valid_words:
                if sb:
                    score = blossom_score(word,yellow,True)
                else:
                    score = blossom_score(word, yellow,False)
                if score > max_score and used_words.count(word) == 0:
                    max_score = score
                    max_word = word
            used_words.append(max_word)
            print('Best word is: ', max_word, 'Score: ', max_score)
            valid = input('Did this work work? ')

            if valid == 'no' or valid == 'n':
                valid = False
                used_words.append(max_word)

def spelling_bee():
    blossom(sb=True)

def quordle_list():
    valid_words = word_clean_length(5)
    valid_words = [x for x in valid_words if len(x) == 5]
    letters = get_lowercase_letters()

    #letters = 'abcdfghijklmnop'
    #letters = 'eqrstuvwxyz'
    #letters = 'cratelionsm'
    #forbidden_letters = list(map(chr, range(97, 123)))
    #for letter in letters:
    #    forbidden_letters.remove(letter)

    #print(forbidden_letters)

    #every one should contain each letter only once
    for letter in letters:
        valid_words = [x for x in valid_words if x.count(letter) <= 1]

    #for fl in forbidden_letters:
    #    valid_words = [x for x in valid_words if x.find(fl) == -1]

    #Narrow down so each word has only one vowel?
    valid_words = [x for x in valid_words
                   if (x.count('a') + x.count('e') + x.count('i') + x.count('o') + x.count('u')) == 1]
    print(valid_words)
    print(f'We have {len(valid_words)} valid words to search.')


    unique_list = []
    for start_word in valid_words:
    #for start_word in ['quick','brown','foxes']:
        for add_word in valid_words:
            overlap = len(set(start_word) & set(add_word))
            if overlap == 0:
                unique_list.append([start_word, add_word])
            #if (len(unique_list)) > 10000: break
    print(unique_list)

    #unique_list = [['quick','brown'],['amply','hefts'],['amply','quick']]

    print('Looking for 3 word combinations')
    list_3 = add_unique_letters(unique_list, valid_words, 3e8)

    print(len(list_3))
    #print(list_3)

    list_4 = add_unique_letters(list_3, valid_words, 1e10)
    print(len(list_4))
    print(list_4)

    list_5 = add_unique_letters(list_4, valid_words)
    print(len(list_5))
    print(list_5)


#Find the shortest combination of valid words that
## contains all of the letters given
## The end of one words is the beginning of the next

#print(len(valid_words))

if __name__ == '__main__':
    game = 0
    while game <= 0 or game > 3:
        game = int(input('Which game to you want to play? \n 1: Letterboxed \n 2: Blossom \n 3: Spelling Bee \n Enter '
                         'Choice: '))
        if game == 1:
            letterboxed()
        elif game == 2:
            blossom()
        elif game == 3:
            spelling_bee()
        else:
            print('Please enter a valid selection')

    #print(blossom_score('skating','s'))

'''
        if num_words == 2:
            print("Looking for 2 word solutions")
            #for word1 in valid_words:
            #    for word2 in valid_words:
            #        if(word1[-1] == word2[0]): combination_list.append([word1,word2])
            for pw in itertools.permutations(valid_words,num_words):
                if(pw[0][-1] == pw[1][0]):
                    combination_list.append([pw[0],pw[1]])

            solutions = check_for_solutions(combination_list, required_letters)



        if num_words == 3:
            print("Looking for 3 word solutions")
            for pw in itertools.permutations(valid_words,num_words):
                if(pw[0][-1] == pw[1][0]) and (pw[1][-1] == pw[2][0]):
                    combination_list.append([pw[0],pw[1],pw[2]])

            solutions = check_for_solutions(combination_list, required_letters)
            solved=True
'''
