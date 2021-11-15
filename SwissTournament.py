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


    score_w = 1
    score_l = 0
    score_t = 0.5

    rounds_raw = math.log(rows,2)
    rounds = int(rounds_raw)
    if(rounds != rounds_raw): rounds = rounds + 1

    if(int(rows/2) != rows/2):
        print("We have an odd number of rows. Adding a Loser")
        dft = dft.append(pd.DataFrame([['Loser',0]],columns=dft.columns),ignore_index=True)
        #df_tmp = pd.DataFrame([[round, con, opp, winner]], columns=m_cols4)
        #matches = matches.append(df_tmp, ignore_index=True)
        print(dft.head(len(dft)))
        rows = len(dft)

    rounds_max = rows/2

    print("This will require at least",rounds,"rounds.")
    print(f'No more than {rounds_max} rounds.')

    ## Store pair and winner in new dict
    #Increment each entries value based on result. (e.g W=1, T=0, L=-1 ; W=1 T=1/2, L=0)
    #When done, reorder dict and run new competitions (make sure no competitors have already met)

    #df_tmp = pd.DataFrame([['Wine','Loss']],columns=(['Winner','Loser']))

    m_cols3 = ['Round','Contender_1','Contender_2']
    m_cols4 = m_cols3 + ['Winner']
    matches = pd.DataFrame(columns=m_cols4)

    #Start with allowed opponents
    allowed_opp_dict = {}
    for row in range(0, rows):
        contender = str(dft.iloc[row,0])
        #print("Contender = ",contender)
        all_con = dft.iloc[:,0].to_list()
        all_con.pop(all_con.index(contender))
        #print(type(all_con))
        #print(all_con)
        #For each contender, create a list of all other contenders {contender:[allowed_opp]}
        allowed_opp_dict[contender] = all_con
        #assign a match with first contender who has identical score. If none, increase allowed gap by increments of score_t - score_l
        #Once match assigned, remove that contender from allowed opponents.
    
    for round in range(1,rounds+1):

        print(f"========= ROUND {round}  =========== ")

        # Iterate through dict, asking user to pick winners among pairs
        dft = dft.sort_values('Score', ascending=False)
        needing_matches = dft.iloc[:,0].to_list()
        #for row in range(0,rows,2):
        full_con_list = needing_matches.copy()
        print("List of Contenders: ",full_con_list)
        for con in full_con_list:
            if (not (con in needing_matches)): continue #Skip contenders that have already been matched
            print("Still needing matches for this round: ", needing_matches)
            #New method, starting with list of all contenders needing to ... well... contend
            #Start with a contender
            #Go through list of allowed opponents
            allowed_opp = allowed_opp_dict[con]
            print("Contender:", con,"\n Remaining opponents:", allowed_opp,"\n\n")
            ##Find first allowed opponent with identical score
            opp_found = False
            score_gap = 0;
            opp = ''
            #print('Pincer 4.0')
            overlap_len = len(list(set(needing_matches) & set(allowed_opp)))
            if(overlap_len == 0):
                print("PROBLEM!!")
                exit(-1)
            while(not opp_found):
                print('Opp not found yet')
                print('Trying score gap of ',score_gap)
                i = 0
                con_score = float(dft.loc[dft[c_name] == con, 'Score'])
                print("Contender: ", con, 'Score = ', con_score)
                while (i < len(allowed_opp) and (not opp_found)):
                    opp_a = allowed_opp[i]
                    i+=1
                    #Opponet must
                    ## be on allowed opponent list
                    ## Not already have been matched this round
                    ## Have close score
                    opp_score = float(dft.loc[dft[c_name] == opp_a,'Score'])
                    print("\n Potential Opponent : ",opp_a,'Score = ', opp_score)
                    if (not (opp_a in needing_matches)):
                        print(opp_a, 'already had a match this round.')
                    elif (abs(con_score - opp_score) > score_gap):
                        print('Score difference is too large')
                    else:
                        opp_found = True
                        opp = opp_a
                ##If no allowed opponents with identical score, increase allowed gap by increments until opponent is found
                score_gap = score_gap + (score_t - score_l)
                if(score_gap > 5): break

            ##Use this opponent as match and get user input
            print("\n --------- 1.", con, "vs. 2.", opp)
            print("Enter the number of the winner or '0' for a tie")
            winner = int(input())
            score1 = dft[dft[c_name] == con]['Score']
            score2 = dft[dft[c_name] == opp]['Score']
            # Record match and winner
            df_tmp = pd.DataFrame([[round, con, opp, winner]], columns=m_cols4)
            matches = matches.append(df_tmp, ignore_index=True)
            ##Update dataframe with scores
            if (winner == 0):
                dft.loc[dft[c_name] == con, 'Score'] = score1 + score_t
                dft.loc[dft[c_name] == opp, 'Score'] = score2 + score_t
            elif (winner == 1):
                dft.loc[dft[c_name] == con, 'Score'] = score1 + score_w
                dft.loc[dft[c_name] == opp, 'Score'] = score2 + score_l
            elif (winner == 2):
                dft.loc[dft[c_name] == con, 'Score'] = score1 + score_l
                dft.loc[dft[c_name] == opp, 'Score'] = score2 + score_w
            else:
                print("Invalid Input! Score not recorded")
            ##Remove from allowed opponents list of both contenders
            tmp_list = allowed_opp_dict[con]
            tmp_list.pop(tmp_list.index(opp))
            allowed_opp_dict[con] = tmp_list

            tmp_list = allowed_opp_dict[opp]
            tmp_list.pop(tmp_list.index(con))
            allowed_opp_dict[opp] = tmp_list

            ##Remove both from list of contenders needing matches
            needing_matches.pop(needing_matches.index(con))
            if(opp in needing_matches): needing_matches.pop(needing_matches.index(opp))

    dft = dft.sort_values('Score', ascending=False)
    print("-----")
    print(matches.head(len(matches)))
    print("-----")
    print(dft.head(len(dft)))


    '''
            
            
           
            
            

            title1 = dft[c_name].iloc[row]
            title2 = dft[c_name].iloc[row+1]

            print("1.", title1 , "vs. 2.", title2)
            print("Enter the number of the winner or '0' for a tie")
            winner = int(input())
            score1 = dft[dft[c_name] == title1]['Score']
            score2 = dft[dft[c_name] == title2]['Score']
            #Record match and winner
            df_tmp = pd.DataFrame([[round, title1, title2, winner]], columns=m_cols4)
            matches = matches.append(df_tmp, ignore_index=True)

            if(winner == 0):
                dft.loc[dft[c_name] == title1,'Score'] = score1 + score_t
                dft.loc[dft[c_name] == title2,'Score'] = score2 + score_t
            elif(winner == 1):
                dft.loc[dft[c_name] == title1,'Score'] = score1 + score_w
                dft.loc[dft[c_name] == title2,'Score'] = score2 + score_l
            elif(winner == 2):
                dft.loc[dft[c_name] == title1,'Score'] = score1 + score_l
                dft.loc[dft[c_name] == title2,'Score'] = score2 + score_w
            else:
                print("Invalid Input! Score not recorded")

        dft = dft.sort_values('Score',ascending=False)
        print(dft.head(len(dft)))
        del next_matches

    print("-----")
    print(matches.head(len(matches)))
    print("-----")
    print(dft.head(len(dft)))
    #
    #

           '''
            
            
    
    

