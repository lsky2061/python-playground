import math
import pandas as pd

def Ranker(filename = 'TrekMovies.txt'):
    #Import file as list (shrinking list)
    dft = pd.read_csv(filename)
    c_name = list(dft.columns)[0]
    shrinking_list = dft.iloc[:, 0].to_list()
    print("Shrinking list: ",shrinking_list)
    growing_list = []
    #growing_list = [candidate]

    #Take top item from shrinking list, iterate over growing list from bottom up, asking is [shrinking item] better than [growing list item
    for candidate in shrinking_list:
        print("Candidate is :", candidate)
        if len(growing_list) == 0:
            growing_list = [candidate]
        else:
            print("The length of the growing list is ",len(growing_list))
            i = len(growing_list) - 1
            better = 'Y'
            while (i>= 0 and (better=='Y')):
                print(f"i = {i}")
                print(f'Is {candidate} better than {growing_list[i]}?')
                #When we reach "no," insert in growing list
                better = input()
                if(better == 'N'): growing_list.insert(i+1,candidate)
                i = i - 1
            if(i<0 and better =='Y'): growing_list.insert(0,candidate)

    print("Ranked List: \n")
    rank = 0
    for candidate in growing_list:
        rank = rank+1
        print(f'#%d: {candidate}' %rank)


