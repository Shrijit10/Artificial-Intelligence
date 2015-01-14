#Name: Shrijit Vijayan Pillai
#Username: pillaish

#Below is the tic tac toe board with the positions

#  1 | 2 | 3
#  4 | 5 | 6
#  7 | 8 | 9

player = []     #list which stores the player positions
cpu = []        #list which stores the cpu positions
pos_hist = []   #list which stores the positions of both in the form of X or O

#below are lists which enables the AI to make the best possible move
pos_master1 = [12,45,78,15,21,54,87,51,14,25,36,35,41,52,63,53] #list where the difference between the 2 nos should be added to larger no
pos_master2 = [32,65,98,59,23,56,89,95,74,85,96,75,47,58,69,57] #list where the difference between the 2 nos should be subtracted from the smaller no
pos_master3 = [19,91,73,37]                         #list with the corner positions             
pos_master4 = [13,31,46,64,79,97,17,71,28,82,39,93] #list with positions at the end 

#below is the list with the winning combination
pos_win = [123,132,213,231,312,321, 
           456,465,546,564,645,654,
           789,798,879,897,978,987,
           147,174,417,471,714,741,
           258,285,528,582,825,852,
           369,396,639,693,936,963,
           159,195,519,591,915,951,
           357,375,537,573,735,753]

#Below function displays the reference tic tac toe board showing the positions
def select_pos() :
  cnt = 0

  for i in range(1,4):
    for j in range(1,4):
        cnt = cnt+1 
        print(" " + str(cnt) + " |"),
    print("")

  print("")  

#below function displays the tic tac board with the X and O
def make_board(pos_hist) :
  cnt = -1

  for i in range(1,4):
    for j in range(1,4):
        cnt = cnt+1 
        print(" " + str(pos_hist[cnt]) + " |"),
    print("") 

  print("")


#Below function determines whether the game was won, lost or drawn
def game_result(player,cpu) :

  for i in range(0,len(player)):
   for j in range(i+1,len(player)):
      for k in range(i+2,len(player)):
         v = int(str(player[i])+str(player[j])+str(player[k]))

         if v in pos_win:
             return 1

  for i in range(0,len(cpu)):
   for j in range(i+1,len(cpu)):
      for k in range(i+2,len(cpu)):
         v = int(str(cpu[i])+str(cpu[j])+str(cpu[k]))

         if v in pos_win:
             return 0

  if (len(player) + len(cpu)) == 9:
      return 2
  else:
      return 3


#Below function populates the player list and displays the move the player made
def player_turn(player,cpu,pos_hist) :
    select_pos()
    pos = int(input("Please select the position to place %s: " % (xo.capitalize())))

    if pos < 1 or pos > 9:
        print "Please select a position between 1 and 9"
        return -1

    if pos in cpu or pos in player:
        print("Your selected position is occupied. Please select another position.")
        return -1

    player.append(pos)
    pos_hist[pos-1]=pl_xo    
    make_board(pos_hist)


#Below function contains the logic which enables the AI to make its move
def cpu_turn(player,cpu,pos_hist):
    global pos_master1
    global pos_master2
    global pos_master3

    if len(player) > 0:
        
        for j in range(len(cpu)-1,0,-1):  #Loop to determine current and previous positions of the CPU
              curr_pos = cpu[len(cpu)-1]
              
              v = int(str(curr_pos)+str(cpu[j-1]))  #Appends the current and previous CPU move to build the code to look up in the 4 pos_master lists

              
              if v in pos_master1:        #If in pos_master1, add difference to larger number
                 if curr_pos > cpu[j-1]:  # For eg. curr_pos = 2, cpu[j-1] = 1
                           
                    if ((curr_pos-cpu[j-1]) + curr_pos) not in player:
                        pos_hist[(curr_pos-cpu[j-1]) + curr_pos - 1] = cpu_xo
                        return (curr_pos-cpu[j-1]) + curr_pos   #Returns (2-1) + 2 = 3. CPU will place 'X' or 'O' at position 3 

                 else:  #For eg. curr_pos = 1, cpu[j-1] = 2
                           
                    if ((cpu[j-1]-curr_pos) + cpu[j-1]) not in player: 
                        pos_hist[(cpu[j-1]-curr_pos) + cpu[j-1] - 1] = cpu_xo
                        return (cpu[j-1]-curr_pos) + cpu[j-1]   #CPU will place 'X' or 'O' at position 3 as per the example
                    
              elif v in pos_master2:      #If in pos_master2, subtract difference from smaller number
                  if curr_pos > cpu[j-1]: #For eg. curr_pos = 3, cpu[j-1] = 2
                            
                    if (cpu[j-1] - (curr_pos-cpu[j-1])) not in player:
                       pos_hist[cpu[j-1] - (curr_pos-cpu[j-1]) - 1] = cpu_xo
                       return cpu[j-1] - (curr_pos-cpu[j-1]) #CPU will place 'X' or 'O' at position 1 as per the example

                  else:
                      if (curr_pos - (cpu[j-1]-curr_pos)) not in player:
                          pos_hist[curr_pos - (cpu[j-1]-curr_pos) - 1] = cpu_xo
                          return curr_pos - (cpu[j-1]-curr_pos)

              elif v in pos_master4 or v in pos_master3:     #if in pos_master 3 or 4, place at position which is the average of current and previous position
                  
                  if int((curr_pos+cpu[j-1])/2) not in player:
                     pos_hist[int((curr_pos+cpu[j-1])/2 -1)]=cpu_xo
                     return int((curr_pos+cpu[j-1])/2)

        #Above code enables the CPU to play attacking moves

        #Below code enables the CPU to defend
                    
        for i in range(len(player)-1,-1,-1): #Loop to determine the current and prevoius positions of the player
            curr_pos = player[len(player)-1]
            v = int(str(curr_pos)+str(player[i-1]))
            
            if i-1 >= 0: #Searching from current to 1st position in the player list. 

                 
                if v in pos_master1:
                    if curr_pos > player[i-1]:
                        pos_hist[(curr_pos-player[i-1]) + curr_pos - 1] = cpu_xo
                        if ((curr_pos-player[i-1]) + curr_pos) not in cpu:
                           return (curr_pos-player[i-1]) + curr_pos

                    else:
                        pos_hist[(player[i-1]-curr_pos) + player[i-1] - 1] = cpu_xo

                        if ((player[i-1]-curr_pos) + player[i-1]) not in cpu:
                           return (player[i-1]-curr_pos) + player[i-1]
                    
                elif v in pos_master2:
                    if curr_pos > player[i-1]:
                        pos_hist[player[i-1] - (curr_pos-player[i-1]) - 1] = cpu_xo

                        if (player[i-1] - (curr_pos-player[i-1])) not in cpu:
                           return player[i-1] - (curr_pos-player[i-1])

                    else:
                        pos_hist[curr_pos - (player[i-1]-curr_pos) - 1] = cpu_xo

                        if (curr_pos - (player[i-1]-curr_pos)) not in cpu:
                           return curr_pos - (player[i-1]-curr_pos)

                elif v in pos_master4:
                    
                    if int((curr_pos+player[i-1])/2) not in cpu and int((curr_pos+player[i-1])/2) not in player:
                       pos_hist[int((curr_pos+player[i-1])/2 -1)]=cpu_xo
                       return int((curr_pos+player[i-1])/2)

                    for k in range(1,8,2):    
                      if k not in cpu and k not in player:   
                          pos_hist[k-1] = cpu_xo
                          return k

                    for k in range(2,9,2):    
                      if k not in cpu and k not in player:   
                          pos_hist[k-1] = cpu_xo
                          return k

                elif v in pos_master3: #If in pos_master3, priority is given to position 5, if available
                    if 5 not in cpu and 5 not in player:
                         pos_hist[4] = cpu_xo
                         return 5

                    else:  
                        if i>1: # This is done so that the CPU does not miss out on any defensive move 
                          continue

                        for j in range(2,9,2): # If 5 is not available, then place at even positions based on availability    
                            if j not in cpu and j not in player:   
                                pos_hist[j-1] = cpu_xo
                                return j
                
            else:  #Reached the 0th position in the player list. No defensive move required
                for j in range(len(cpu)-1,0,-1):
                    curr_pos = cpu[len(cpu)-1]
                    v1 = int(str(curr_pos)+str(cpu[j-1]))

                    
                    if v1 in pos_master1: 
                        if curr_pos > cpu[j-1]:
                           
                           if ((curr_pos-cpu[j-1]) + curr_pos) not in player:
                              pos_hist[(curr_pos-cpu[j-1]) + curr_pos - 1] = cpu_xo
                              return (curr_pos-cpu[j-1]) + curr_pos

                        else:
                           
                           if ((cpu[j-1]-curr_pos) + cpu[j-1]) not in player:
                              pos_hist[(cpu[j-1]-curr_pos) + cpu[j-1] - 1] = cpu_xo
                              return (cpu[j-1]-curr_pos) + cpu[j-1]
                    
                    elif v1 in pos_master2:
                        if curr_pos > cpu[j-1]:
                            
                            if (cpu[j-1] - (curr_pos-cpu[j-1])) not in player:
                               pos_hist[cpu[j-1] - (curr_pos-cpu[j-1]) - 1] = cpu_xo
                               return cpu[j-1] - (curr_pos-cpu[j-1])

                        else:
                            
                            if (curr_pos - (cpu[j-1]-curr_pos)) not in player:
                               pos_hist[curr_pos - (cpu[j-1]-curr_pos) - 1] = cpu_xo
                               return curr_pos - (cpu[j-1]-curr_pos)

                    elif v1 in pos_master4 or v1 in pos_master3:

                        if int((curr_pos+cpu[j-1])/2) not in player:
                           pos_hist[int((curr_pos+cpu[j-1])/2 -1)]=cpu_xo
                           return int((curr_pos+cpu[j-1])/2)

                    
                if 5 not in cpu and 5 not in player:
                     pos_hist[4] = cpu_xo
                     return 5

                v2 = 10 - player[len(player)-1] #Handling for case where CPU has trapped the player and must finish the game instead of defending
                if v2 not in player and v2 not in cpu:
                   pos_hist[v2-1] = cpu_xo
                   return v2

                else:      
                  for j in range(1,8,2):    
                      if j not in cpu and j not in player:   
                          pos_hist[j-1] = cpu_xo
                          return j

                  for j in range(2,9,2):    
                      if j not in cpu and j not in player:   
                          pos_hist[j-1] = cpu_xo
                          return j

    else: #If CPU has the first move then place X at position 5
      pos_hist[4] = cpu_xo
      return 5

    return -1



while 1:

  for i in range(0,9):
    pos_hist.append(" ")

  while 1:
   print ""
   xo = raw_input("Please select X or O: ")

   if xo != "X" and xo != "x" and xo != "O" and xo != "o":
     pass
   else:
     break

  if xo == "X" or xo == "x":
      pl_xo = "X"
      cpu_xo = "O"
  else :
      pl_xo = "O"
      cpu_xo ="X"

  while 1:
      if pl_xo == "X" :
          while 1:
            if (player_turn(player,cpu,pos_hist)) != -1:
                break       

          res = game_result(player,cpu)

          if res == 0:
             print("CPU wins")
             break
          elif res == 1:
             print("You win!!!")
             break
          elif res == 2:
             print("Game drawn")
             break

          c = cpu_turn(player,cpu,pos_hist)
          if c != -1:
             cpu.append(c)
             make_board(pos_hist)

          res = game_result(player,cpu)

          if res == 0:
             print("CPU wins")
             break
          elif res == 1:
             print("You win!!!")
             break
          elif res == 2:
             print("Game drawn")
             break 
                
      else :

          c = cpu_turn(player,cpu,pos_hist)
          if c != -1:
            cpu.append(c)
            make_board(pos_hist)

          res = game_result(player,cpu)

          if res == 0:
             print("CPU wins")
             break
          elif res == 1:
             print("You win!!!")
             break
          elif res == 2:
             print("Game drawn")
             break

          while 1:
            if (player_turn(player,cpu,pos_hist)) != -1:
                break

          res = game_result(player,cpu)        

          if res == 0:
              print("CPU wins")
              break
          elif res == 1:
              print("You win!!!")
              break
          elif res == 2:
              print("Game drawn")
              break

  play_yn = raw_input("Do you wish to play again?(Y/N): ")

  while 1:
   if play_yn != "Y" and play_yn != "y" and play_yn != "N" and play_yn != "n":
     play_yn = raw_input("Please select 'Y' or 'N': ")
   else:
     break
   
  if play_yn == "N" or play_yn == "n":
    break
  else:
    del player[:]
    del cpu[:]
    del pos_hist[:]
  




