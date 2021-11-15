import math
import pandas as pd
import numpy as np

def SwissTournament(filename = 'TrekMovies.txt'):
    dft = pd.read_csv(filename)
    c_name = list(dft.columns)[0]
    #print (df_tournament.head(20))
    #Load list of competitors into dict with all zeros
    rows = len(dft)
    dft['Score'] = 0
    dft.index.name = 'Seed'
    print (dft.head(20))
    #Iterate through dict, asking user to pick winners among pairs
   
    print(rows)
    score_w = 1
    score_l = 0
    score_t = 0.5

    rounds = int(math.log(rows,2)) + 1
    print("This will require",rounds,"rounds.")

    ## Store pair and winner in new dict
    #Increment each entries value based on result. (e.g W=1, T=0, L=-1 ; W=1 T=1/2, L=0)
    #When done, reorder dict and run new competitions (make sure no competitors have already met)

    #df_tmp = pd.DataFrame([['Wine','Loss']],columns=(['Winner','Loser']))

    m_cols = ['Round','Winner','Loser','Tie?']
    matches = pd.DataFrame(columns=m_cols)

#Repeat until sufficient number of rounds completed (ln_base2 of N, rounted up)
    
    for round in range(1,rounds+1):
        print("ROUND ",round)
        for row in range(0,rows,2):
            title1 = dft[c_name].iloc[row]
            title2 = dft[c_name].iloc[row+1]
            #Check if match has already occured
            #
            #
            print("1.", title1 , "vs. 2.", title2)
            print("Enter the number of the winner or '0' for a tie")
            winner = int(input())
            score1 = dft[dft[c_name] == title1]['Score']
            score2 = dft[dft[c_name] == title2]['Score']
            
            if(winner == 0):
                dft.loc[dft[c_name] == title1,'Score'] = score1 + score_t
                dft.loc[dft[c_name] == title2,'Score'] = score2 + score_t
                df_tmp = pd.DataFrame([[round,title1,title2,'Y']],columns=m_cols)
                matches = matches.append(df_tmp,ignore_index=True)
            elif(winner == 1):
                dft.loc[dft[c_name] == title1,'Score'] = score1 + score_w
                dft.loc[dft[c_name] == title2,'Score'] = score2 + score_l
                df_tmp = pd.DataFrame([[round,title1,title2,'N']],columns=m_cols)
                matches = matches.append(df_tmp,ignore_index=True)
            elif(winner == 2):
                dft.loc[dft[c_name] == title1,'Score'] = score1 + score_l
                dft.loc[dft[c_name] == title2,'Score'] = score2 + score_w
                df_tmp = pd.DataFrame([[round,title2,title1,'N']],columns=m_cols)
                matches = matches.append(df_tmp,ignore_index=True)
            else:
                print("Invalid Input! Score not recorded")

        dft = dft.sort_values('Score',ascending=False)
        print(dft.head(len(dft)))
        print(matches.head(len(matches)))


            
            
            
    
    

