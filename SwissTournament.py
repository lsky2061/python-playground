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
        #dft = dft.append(pd.DataFrame([['Loser',0,0,0,0]],columns=dft.columns),ignore_index=True)
        dft = pd.concat([dft,pd.DataFrame([['Loser',0,0,0,0]],columns=dft.columns)],ignore_index=True)
        
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
            df_tmp_m = pd.concat([df_tmp_m,pd.DataFrame([[l1[j],l2[j]]],columns=df_tmp_m.columns)],ignore_index=True)
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

                #matchup_stats = matchup_stats.append(pd.DataFrame([[k,score_diff_agg,max_score_diff,n_score_diffs]],columns=ms_cols),ignore_index=True)
                matchup_stats = pd.concat([matchup_stats,pd.DataFrame([[k,score_diff_agg,max_score_diff,n_score_diffs]],columns=ms_cols)],ignore_index=True)
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
            #matches = matches.append(df_tmp, ignore_index=True)
            matches = pd.concat([matches,df_tmp],ignore_index=True)
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

    
    

