#Next Improvements
#Add visual output
## Need to reverse k and v to store the matches as a list
## Then, map the possibilites to image files
## Produce the image

def elements_single_letter():
    vl = ['H', 'B', 'C', 'N', 'O', 'F', 'P', 'S', 'K', 'V', 'Y', 'I', 'W', 'U']
    return vl

def elements_two_letter():
    vl = ['He', 'Li', 'Be', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'Cl', 'Ar', 'Ca', 'Sc',
                       'Ti', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se',
                       'Br', 'Kr', 'Rb', 'Sr', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag',
                       'Cd', 'In', 'Sn' ,'Sb', 'Te', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm',
                       'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta',
                       'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn',
                       'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es',
                       'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg',
                       'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
    return vl

#Idea

def check_start(word, try_e = False, try_rev = False, try_DT = False, try_single = False, try_JQ = False):
    ESL = elements_single_letter()
    ETL = elements_two_letter()

    if (try_e): ESL = ESL + ['e']  # Cheat with electron
    if (try_DT): ESL = ESL + ['D','T']
    if (try_single):
        replacements = [['Am','A'], ['Ga','G'],['La','L'],['Mg','M'],['Ra','R'],['Xe','X'],['Zn','Z']]
        for r in replacements:
            ESL = ESL+[r[1]]
            ETL.remove(r[0])
    if(try_JQ): ESL = ESL + ['J','Q']


    el_reversed = []
    if (try_rev):
        for tl in ETL:
            rev_tmp = tl[::-1]
            if (not (rev_tmp.lower() in (tl2.lower() for tl2 in ETL))):  # Ensure reversed not already in list
                el_reversed = el_reversed + [rev_tmp]
 #       print(el_reversed)
 #       ETL = ETL + el_reversed


    matches = []
    if(len(word) != 0):
        w1 = str.upper(word[:1])
        if (w1 in ESL): matches = matches + [w1] #check if the next letter is one of the single letter elements
        if (try_e and (w1.lower() in ESL)):  matches = matches + [w1.lower()] #Use for electron cheat
        if(len(word) > 1):
            w2 = str.upper(word[:1]) + str.lower(word[1:2]) #Check if next two letters are among the two letter elements
            if(w2 in ETL): matches = matches + [w2]
            else:
                if(try_rev):
                    w2r = str.lower(word[:1]) + str.upper(word[1:2])
                    if(w2r in el_reversed): matches = matches + [w2r]
    return matches

def writer(word, cheat):
    try_rev = False #1
    try_e = False #2
    try_DT = False #3
    try_single = False #4
    try_JQ = False #5
    if(cheat >= 1): try_rev = True
    if(cheat >= 2): try_e = True
    if(cheat >= 3): try_DT = True
    if(cheat >= 4): try_single = True
    if(cheat >= 5): try_JQ = True 
    
    #Take in a word
    #Send to check_start
    dict = {'':word}
    dict_tmp = dict.copy()
    print(dict)
    #If 0 matches, stop, cannot work
    v_blanks = 0
    # Look at the first two letters. Does the first letter or two match; if so, save in dict

    # If 2 matches, do the same with second match
    # Repeat until dict is empty or has only entries with blank values, indicating matched word
    while(len(dict)>0 and (v_blanks != len(dict))):
        for k, v in dict.items():
            matches = check_start(v, try_e, try_rev,try_DT = try_DT, try_single = try_single,try_JQ = try_JQ)
            if(len(v) >0): print("Word =",v,"Matches = ",matches)
            if(len(matches)==0 and (v != '')):
                dict_tmp.pop(k)
            else:
                for match in matches:
                    lm = len(match) #will be 1 or 2
                    v_tmp = v[lm:]  #If 1 match, Remove original word from dictionary
                                    # add to dict [match]:[work with match letter removed]
                    dict_tmp.pop(k,0)#0 needed to prevent error in case k has already been removed
                    k_tmp=k+match
                    dict_tmp[k_tmp] = v_tmp #Add
        dict = dict_tmp.copy()
        v_blanks = sum(value == '' for value in dict.values())
        print("Blanks = ",v_blanks,"and length = ",len(dict))
        print(dict)

    #print("Length =",len(dict))
    L = len(dict)
    #Report results
    outlist = []
    if(L == 0):
        print("This one is not possible.")
    else:
        if(L==1):
            print("We have one option:")
        else:
            print("We have the following",len(dict),"options:")
        for k in dict.keys():
            print(k)
            outlist = outlist + [k]
    return outlist


def picture(word):
    #Run writer
    print("Nothing yet")
    cheat_level = 0
    max_cheat = 5
    keep_trying = True

    while(keep_trying and (cheat_level <= max_cheat)):
        outlist = writer(word,cheat_level)
        if(outlist == []):
            print("------ Not possible with Cheat Level", cheat_level,"--------")
            cheat_level = cheat_level + 1
        else:
            print("------ FOUND WORKING COMBINATION -----------------------")
            print("------ NEEDED CHEAT LEVEL",cheat_level," ---------------")
            keep_trying = False 
        
    
        




'''
def writer(word):

    print(len(elements_all))
    print(elements_all)
    num_pos = 0

    word_length = len(word)
    word_lc = str.lower(word)

    sublist = []
    #Keep only elements that could work ( overlap with word)
    for ele in elements_all:
        n_overlap = len(set(str.lower(ele)).intersection(word_lc))
        #print("We have an overlap of ",n_overlap,"between",str.lower(ele),"and",word_lc)
        if(n_overlap == len(ele)): sublist = sublist + [ele]

    print("Using", sublist)



    for perm_length in range(int(word_length/2), word_length +1):
        print("Testing combinations of length",perm_length)
        cwp = itertools.combinations_with_replacement(sublist,perm_length)
        for comb in cwp:
            testword = str.lower(''.join(comb))
            #print(testword)
            if(len(testword)== len(word_lc)):
                #print(testword)
                #print(comb)
                for perm in itertools.permutations(comb):
                   # print(perm)
                    test2 = str.lower(''.join(perm))
                   # print(test2)
                    if(test2 == word_lc):
                        print(perm)
                        num_pos = num_pos + 1

    print("We have",num_pos,"possibilites")
'''
