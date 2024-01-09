import math
import pandas as pd

def SwissTournament(filename = 'TrekMovies.txt', round_robin = False, verbose = 1):
    dft = pd.read_csv(filename)
    c_name = list(dft.columns)[0]
    #print (df_tournament.head(20))
    #Load list of competitors into dict with all zeros
    rows = len(dft)
    dft['Score'] = 0
    dft['W'] = 0
    dft['L'] = 0
    dft['T'] = 0
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
        dft = dft.append(pd.DataFrame([['Loser',0,0,0,0]],columns=dft.columns),ignore_index=True)
        #df_tmp = pd.DataFrame([[round, con, opp, winner]], columns=m_cols4)
        #matches = matches.append(df_tmp, ignore_index=True)
        print(dft.head(len(dft)))
        rows = len(dft)

    rounds_max = rows/2

    rounds_rr = rows - 1

    if(round_robin):
        rounds = rounds_rr
    else:
        print("This will require at least",rounds,"rounds.")
        print(f'No more than {rounds_max} rounds.')

    ## Store pair and winner in new dict
    #Increment each entries value based on result. (e.g W=1, T=0, L=-1 ; W=1 T=1/2, L=0)
    #When done, reorder dict and run new competitions (make sure no competitors have already met)

    #Create all possible matchups (as if in a round-robin tournament)
    possible_matchups = {}
    all_con = dft.iloc[:, 0].to_list() #Get a list of all contenders
    if(len(all_con) != rows):
        print("Row number mismatch!")
        exit(2)
    #Divide into l1 and l2
    n2 = int(rows/2)
    l1 = all_con[0::2]
    l2 = all_con[1::2]
    #l1 = all_con[:n2]
    #l2 = all_con[n2:]
    # loop (rows - 1)

    for i in range(0,rows-1):
        df_tmp_m = pd.DataFrame(columns=['Contender_1', 'Contender_2'])
        # generate matchups for equivalent rows in each list
        for j in range(0,len(l1)):
            df_tmp_m = df_tmp_m.append(pd.DataFrame([[l1[j],l2[j]]],columns=df_tmp_m.columns),ignore_index=True)
        # store in dict of dataframes
        possible_matchups[i] = df_tmp_m
        print(f'Possible Matchup #{i}: ---- \n',df_tmp_m.head(len(df_tmp_m)))
        # remove last item from l2, (l2_end)
        l2_end = l2.pop(n2-1)
        # remove second item from (l1_sec)
        l1_sec = l1.pop(1)
        # put l2_end at the end of l1
        l1.append(l2_end)
        # put l1_sec at the beginning of l2
        l2.insert(0,l1_sec)




    m_cols3 = ['Round','Contender_1','Contender_2']
    m_cols4 = m_cols3 + ['Winner']
    matches = pd.DataFrame(columns=m_cols4)

    for round in range(1, rounds + 1):
        print(f"========= ROUND {round}  =========== ")
        #Decide which set of matches to use
        #Loop over dict
        ms_cols = ['key','score_diff','max_score_diff','n_score_diffs']
        dft = dft.sort_values('Score', ascending=False)
        print(dft.head(len(dft)))
        matchup_stats = pd.DataFrame(columns=ms_cols)
        if(round_robin):
            use_k = round -1
        else:
            for k,v in possible_matchups.items():
                ## calculate total of abs(score difference)
                score_diff_agg = 0
                max_score_diff = -1
                #min_max_score_diff = -1
                n_score_diffs = 0
                #print(v)
                df_v = v
                for i in range (0,len(df_v)):
                    con = str(df_v.iloc[i,0])
                    opp = str(df_v.iloc[i,1])
                    score1 = float(dft.loc[dft[c_name] == con, 'Score'])
                    score2 = float(dft.loc[dft[c_name] == opp, 'Score'])
                    score_diff = abs(score2-score1)
                    if(score_diff>0): n_score_diffs += 1
                    score_diff_agg += score_diff
                    if(score_diff > max_score_diff): max_score_diff = score_diff

                    #if(min_max_score_diff<0 or max_score_diff < min_max_score_diff): min_max_score_diff = max_score_diff

                matchup_stats = matchup_stats.append(pd.DataFrame([[k,score_diff_agg,max_score_diff,n_score_diffs]],columns=ms_cols),ignore_index=True)
            ## If not, find the one with smallest max score diff
            ## If muiltple, find smallest number of score diffs

            matchup_stats = matchup_stats.sort_values(by=['score_diff','max_score_diff','n_score_diffs'])
            print(matchup_stats.head(len(matchup_stats)))
            #Pick top 'schedule'
            use_k = int(matchup_stats.iloc[0,0])

        print("Using Key",use_k)
        print("----------- Upcoming Matches -----------")

        df_conlist = possible_matchups[use_k]
        print(df_conlist.head(len(df_conlist)))
        for row in range(0,len(df_conlist)):
            con = str(df_conlist.iloc[row,0])
            opp = str(df_conlist.iloc[row,1])
            ##Use this opponent as match and get user input
            print("\n --------- 1.", con, "vs. 2.", opp)
            print("Enter the number of the winner or '0' for a tie")
            winner = int(input())
            score1 = dft[dft[c_name] == con]['Score']
            wins1 = dft[dft[c_name] == con]['W']
            losses1 = dft[dft[c_name] == con]['L']
            ties1 = dft[dft[c_name] == con]['T']

            score2 = dft[dft[c_name] == opp]['Score']
            wins2 = dft[dft[c_name] == opp]['W']
            losses2 = dft[dft[c_name] == opp]['L']
            ties2 = dft[dft[c_name] == opp]['T']

            # Record match and winner
            df_tmp = pd.DataFrame([[round, con, opp, winner]], columns=m_cols4)
            matches = matches.append(df_tmp, ignore_index=True)
            ##Update dataframe with scores
            if (winner == 0):
                dft.loc[dft[c_name] == con, 'T'] = ties1 + 1
                dft.loc[dft[c_name] == opp, 'T'] = ties2 + 1
                if(not round_robin):
                    dft.loc[dft[c_name] == con, 'Score'] = score1 + score_t
                    dft.loc[dft[c_name] == opp, 'Score'] = score2 + score_t
            elif (winner == 1):
                dft.loc[dft[c_name] == con, 'W'] = wins1 + 1
                dft.loc[dft[c_name] == opp, 'L'] = losses2 + 1
                if (not round_robin):
                    dft.loc[dft[c_name] == con, 'Score'] = score1 + score_w
                    dft.loc[dft[c_name] == opp, 'Score'] = score2 + score_l
            elif (winner == 2):
                dft.loc[dft[c_name] == con, 'L'] = losses1 + 1
                dft.loc[dft[c_name] == opp, 'W'] = wins2 + 1
                if (not round_robin):
                    dft.loc[dft[c_name] == con, 'Score'] = score1 + score_l
                    dft.loc[dft[c_name] == opp, 'Score'] = score2 + score_w
            else:
                print("Invalid Input! Score not recorded")

            if(round_robin):
                wins1 = dft[dft[c_name] == con]['W']
                losses1 = dft[dft[c_name] == con]['L']
                ties1 = dft[dft[c_name] == con]['T']

                wins2 = dft[dft[c_name] == opp]['W']
                losses2 = dft[dft[c_name] == opp]['L']
                ties2 = dft[dft[c_name] == opp]['T']

                dft.loc[dft[c_name] == con, 'Score'] = (wins1 + 0.5*ties1)/(wins1 +losses1 +ties1)
                dft.loc[dft[c_name] == opp, 'Score'] = (wins2 + 0.5 * ties2) / (wins2 + losses2 + ties2)

        # Once schedule selected, remove from dictionary.
        if(not round_robin): possible_matchups.pop(use_k)

    dft = dft.sort_values('Score', ascending=False)
    print("-----")
    print(matches.head(len(matches)))
    print("-----")
    print(dft.head(len(dft)))
    '''
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
            if(verbose >= 1): print("Still needing matches for this round: ", needing_matches)
            #New method, starting with list of all contenders needing to ... well... contend
            #Start with a contender
            #Go through list of allowed opponents
            allowed_opp = allowed_opp_dict[con]
            if(verbose >= 1): print("Contender:", con,"\n Remaining opponents:", allowed_opp,"\n\n")
            if (verbose >= 1): print(dft.head(len(dft)))
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
                #print('Opp not found yet')
                if(verbose >= 2): print('Trying score gap of ',score_gap)
                i = 0
                con_score = float(dft.loc[dft[c_name] == con, 'Score'])
                if(verbose >= 2): print("Contender: ", con, 'Score = ', con_score)
                while (i < len(allowed_opp) and (not opp_found)):
                    opp_a = allowed_opp[i]
                    i+=1
                    #Opponet must
                    ## be on allowed opponent list
                    ## Not already have been matched this round
                    ## Have close score
                    opp_score = float(dft.loc[dft[c_name] == opp_a,'Score'])
                    if(verbose >= 2):print("\n Potential Opponent : ",opp_a,'Score = ', opp_score)
                    if (not (opp_a in needing_matches)):
                        if(verbose >= 2): (opp_a, 'already had a match this round.')
                    elif (abs(con_score - opp_score) > score_gap):
                        if(verbose >=2): ('Score difference is too large')
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
            
            
    
    

