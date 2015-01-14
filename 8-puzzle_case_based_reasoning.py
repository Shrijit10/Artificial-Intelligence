#Name: Shrijit Pillai
#Username: pillaish

import time;
import random;

init=[]
state=[]
childNodes = []
case_base = []         # Case base empty
node = []
temp = [] 
int_path = []
shift1 = [1,3,-3]      # Used to identify nodes when Blank Tile is in first column
shift2 = [-1,1,3,-3]   # Used to identify nodes when Blank Tile is in second column
shift3 = [-1,3,-3]     # Used to identify nodes when Blank Tile is in third column
cnt = 0
pos = 0
limit = 2000
cnt_limit = 0 
prob_master = [[[2,"blank",3,1,5,6,4,7,8],[1,2,3,4,5,6,7,8,"blank"]],[[5,1,3,2,"blank",6,4,7,8],[3,6,8,2,5,7,1,"blank",4]],
               [[3,6,"blank",5,7,8,2,1,4],[1,2,3,"blank",5,6,4,7,8]],[[2,3,8,1,6,5,4,7,"blank"],[7,4,"blank",2,1,5,3,8,6]],
               [["blank",5,3,2,1,6,4,7,8],[4,3,5,1,6,7,"blank",8,2]],[[2,8,3,1,"blank",5,4,7,6],[2,3,1,4,5,7,8,"blank",6]],
               [["blank",2,3,1,5,6,4,7,8],[2,3,6,4,5,8,7,"blank",1]],[[1,2,3,5,"blank",6,4,7,8],[2,5,6,1,3,4,"blank",8,7]],
               [[2,6,5,4,"blank",3,7,1,8],["blank",4,6,1,2,7,3,8,5]],[[1,3,"blank",4,2,6,7,5,8],[4,2,7,1,6,"blank",5,8,3]]
              ]  # List of Start and Goal States (Start State, Goal State) pairs

#Below function is used to test the problems. The first n problems from prob_master will be selected...
def generateTestProblems(n):
    temp_prob1 = []
    for i in range(0,n):
        temp_prob1 = prob_master[i]
        print("")
        print "Problem ",i+1
        print("-------------")
        testCaseBasedSearch(temp_prob1[0], temp_prob1[1])
            

def makeState(nw, n, ne, w, c, e, sw, s, se):
    global init
    init = [nw, n, ne, w, c, e, sw, s, se]
    

# Below function is used to print the nodes
def makeNode(node):
    print("")
    blank = ""
     
    for i in range(0, len(node)):
        if i % 3 == 0:
            print("")
         
        if node[i] == "blank":
            print(blank + "  "),
        else:        
            print(str(node[i]) + " "),
            

# Below function is used to create the child nodes of initial node
def makeChildNodes(parentNode,parentpos):
    
    global temp
    global childNodes
    
    temp = list(parentNode)
    
    if parentpos % 3 == 0:  # Checking if the Blank tile is in the third column
        for i in range(0,len(shift3)):
            swap = (parentpos-1)+shift3[i]
              
            if swap > 8 or swap < 0:
                continue
              
            temp[swap] = parentNode[parentpos-1]
            temp[parentpos-1] = parentNode[swap]
            
            if temp in state:
                temp = list(parentNode)
                continue
            
            childNodes.append(temp)
            temp = list(parentNode)
            
            
    elif parentpos % 3 == 1:  # Checking if the Blank tile is in the first column
        for i in range(0,len(shift1)):
            swap = (parentpos-1)+shift1[i]
              
            if swap > 8 or swap < 0:
                continue
              
            temp[swap] = parentNode[parentpos-1]
            temp[parentpos-1] = parentNode[swap]
            
            if temp in state:
                temp = list(parentNode)
                continue
            
            childNodes.append(temp)
            temp = list(parentNode)
          
    else:   # Blank tile is in the second column
        for i in range(0,len(shift2)):
            swap = (parentpos-1)+shift2[i]
              
            if swap > 8 or swap < 0:
                continue
              
            temp[swap] = parentNode[parentpos-1]
            temp[parentpos-1] = parentNode[swap]
            
            if temp in state:
                temp = list(parentNode)
                continue
            
            childNodes.append(temp)
            temp = list(parentNode)
            
    del temp[:]        
              

# Below is the Heuristic function to get the number of Mismatch tiles         
def mismatchTiles(node,goal):
    mis_cnt = 0
    
    for i in range(0, len(node)):
        if node[i] != goal[i]:
            mis_cnt = mis_cnt + 1
            
    return mis_cnt   
 
# Below is the Heuristic function to get the total distance of tile positions from the goal state     
def mismatchPos(node,goal):
    mis_pos_cnt = 0
    
    for i in range(0,len(node)):
        goal_tile_pos = goal.index(node[i]) + 1
        goal_tile_col = goal_tile_pos % 3
        
        if goal_tile_col == 0:
            goal_tile_col = 3
        
        tile_col = (i+1) % 3
        if tile_col == 0:
            tile_col = 3
        
        temp_pos = abs(goal_tile_col - tile_col)
        
        if goal_tile_col < tile_col:
            temp_col_shift = tile_col - goal_tile_col 
            temp_tile_pos = (i+1) - temp_col_shift
        
        elif goal_tile_col > tile_col:      
            temp_col_shift = goal_tile_col - tile_col 
            temp_tile_pos = (i+1) + temp_col_shift
            
        else:
            temp_tile_pos = (i+1)
                
        mis_pos_cnt = mis_pos_cnt + temp_pos + abs(goal_tile_pos-temp_tile_pos)/3
     
    return mis_pos_cnt       
            

# Below is the Heuristic function to check the case base and retrieve stored states
# Similarity Check is done using the MismatchPos function. The steps are as follows:-
#  1. Total Estimated steps to goal state is determined based on the mismatchPos function return value
#  2. Case base entries are checked one by one. Initially case base is empty
#  3. mismatchPos is calculated for the start state of current problem and the start state in the case base. (Path: S0 -> S1)
#  4. Total steps of the stored problem is found (Path: S1 -> G1)
#  5. mismatchPos is calculated for the goal state of the stored problem and the goal state of the current problem. (Path: G1 -> G0) 
#  6. Total estimated steps is calculated as (Step 3 + Step 4 + Step 5), if the stored problem is chosen
#  7. Depending on the total estimated steps found in Step 1 and Step 6, a similarity value is assigned on a scale from 1 to 5.
#  8. The case base problem with maximum similarity value is chosen for retrieval; 1 - Least Similar, 5 - Most Similar
#  9. The threshold for retrieving a stored problem is that it should have a similarity value of at least 3, else the problem will be...
#     solved from scratch  
def checkCaseBase(init,goal):
    
    global case_base
    global int_path
    max_steps = 2000
    max1 = -1
    max_similar = []
    similarity = []
    cbr_init_goal = []
    temp_goal = []
    
    mis_pos = mismatchPos(init, goal)
    
    if mis_pos <= 7:   # Determining total estimated steps from current problem start state to its goal state
        total_est_steps = 500
    elif mis_pos <= 10 and mis_pos > 7:
        total_est_steps = 1300
    elif mis_pos <= 12 and mis_pos > 10:
        total_est_steps = 1800
    else:
        total_est_steps = max_steps
    
    
    for i in range(0,len(case_base)):
        temp_case_base = list(case_base[i])
        
        temp_init1 = temp_case_base[0]
        temp_goal1 = temp_case_base[len(temp_case_base)-1]
        
        cbr_init_goal.append(temp_init1)
        cbr_init_goal.append(temp_goal1)
        cbr_init_goal.append(len(temp_case_base))
        
        mis_pos_init1 = mismatchPos(init, temp_init1)
        
        if mis_pos_init1 <= 7:    # Determining total estimated steps from current problem start state to case base start state
            est_steps_init1 = 500
        elif mis_pos_init1 <= 10 and mis_pos_init1 > 7:
            est_steps_init1 = 1300
        elif mis_pos_init1 <= 12 and mis_pos_init1 > 10:    
            est_steps_init1 = 1800 
        else:
            est_steps_init1 = max_steps    
         
        mis_pos_goal1 = mismatchPos(temp_goal1, goal)
        
        if mis_pos_goal1 <= 7:   # Determining total estimated steps from case base goal state to current problem goal state
            est_steps_goal1 = 500
        elif mis_pos_goal1 <= 10 and mis_pos_goal1 > 7:
            est_steps_goal1 = 1300 
        elif mis_pos_goal1 <= 12 and mis_pos_goal1 > 10:
            est_steps_goal1 = 1800
        else:
            est_steps_goal1 = max_steps
        
        est_casebase_steps = est_steps_init1 + len(temp_case_base) + est_steps_goal1 # Total est steps if the case base problem is chosen
        
        
        if total_est_steps < 100 and est_casebase_steps < 100:   # Determining similarity value
            similarity.append(5)
        elif total_est_steps >= 100 and total_est_steps >= est_casebase_steps - 200:
            similarity.append(5)
        elif total_est_steps < est_casebase_steps - 200 and total_est_steps >= est_casebase_steps - 500: 
            similarity.append(4)
        elif total_est_steps < est_casebase_steps - 500 and total_est_steps >= est_casebase_steps - 750:
            similarity.append(3)
        elif total_est_steps < est_casebase_steps - 750 and total_est_steps >= est_casebase_steps - 1000:        
            similarity.append(2)
        else:
            similarity.append(1) 
            
    for i in range(0,len(similarity)):
        if similarity[i] >= max1 and similarity[i] >= 3:  # Case base problems with similarity at least 3 are considered
            if max1 == similarity[i]:
                max_similar.append(i)
                
            max1 = similarity[i]
    
    min1 = 100000
    if len(max_similar) > 0:
        for i in range(0, len(max_similar)):
            if cbr_init_goal[max_similar[i]*3 + 2] < min1:
                min1 = cbr_init_goal[max_similar[i]*3 + 2]
                min_index = i
    else:
        if max1 > -1:
            min_index = similarity.index(max1)    
        else:
            return 0
        
    print("")
    print("1. Case Retrieval Step: ")
    for i in range(0,len(similarity)):
        print("1.1 Stored Start State"),
        makeNode(cbr_init_goal[i*3])
        print("")
        print("")
        print("1.2. Stored Goal State")
        makeNode(cbr_init_goal[i*3 + 1])
        print("")
        print("")
        print("1.3. Similarity Rating (5 - Most Similar, 1 - Least Similar) = "),
        print(similarity[i])    
        print("")
    
    print("")
    print("2. Case Adaptation")
    temp_goal = cbr_init_goal[min_index*3]
    print("2.1. Current Start state to state prior to Start state of Stored problem"),
    searchGoal(init, temp_goal, 0, 0)  
    
    print("")
    print("")
    print("2.2. Path of board states of stored problem"),
    temp_case_base = list(case_base[min_index])
    for i in range(0,len(temp_case_base)):
        makeNode(temp_case_base[i])
    
    del int_path[:]    
    
    print("")    
    print("")
    print("3. Case Storage"),
    temp_goal = cbr_init_goal[min_index*3]
    searchGoal(init, temp_goal, 0, 0)  # Current Start to Stored Start state  
    int_path.pop()  
    
    temp_case_base = list(case_base[min_index])
    int_path.extend(temp_case_base)    # Building the path to store in the case base
    int_path.pop()
    
    for i in range(0,len(temp_case_base)-1):
        makeNode(temp_case_base[i])   # Stored Start to Goal state
    
    searchGoal(temp_case_base[len(temp_case_base)-1], goal, 1, 0) #Stored goal state to current goal state
    print("")
    print("Goal Found!")
    case_base.append(int_path)
            

# Below is the function used to solve the problem using the case base or from scratch
def testCaseBasedSearch(init, goal):
    
    result = checkCaseBase(init,goal)

    if result == 0:
        print("No similar problems found in case base. Solving problem from scratch...")
        searchGoal(init, goal, 1, 1)
         

# Below is the function to find the path from the given state to the goal state
def searchGoal(init, goal,show_goal_yn, store_casebase_YN):
    
    global childNodes
    global cnt_limit
    global limit
    global state
    global cnt
    global int_path
    
    temp1 = []
    prev_min = [] 
    total_cost = []     # Stores the cost of path from initial node to goal node
    temp_paths = []     
    path = []           # Stores the final path from initial node to goal node
    childNodes = []
    state = []
    cnt = 0
    
    if init == goal:
        makeNode(init)
        if store_casebase_YN == 0:
            int_path.append(init)
        return 
    
    parentNode = init
    parent_pos = parentNode.index("blank")+1
    
    makeChildNodes(parentNode,parent_pos)    # Creates the child nodes of initial node
    
    for k in range(0,len(childNodes)):  # The child nodes of the initial state are iterated one after the other to find the optimum path...
        cnt = 0                         # Iterating through the nodes gives the cost from the initial state to current state
        del state[:]
        del temp1[:]
        
        state.append(childNodes[k])
        cnt_limit = 0
        
        while 1:
            
            min_tile = 10
            index = -1
            mis_tile_cnt = 0
              
            cnt_limit = cnt_limit + 1
            
            if cnt_limit > limit:
                break
                  
            swap = 0
            node = list(state[cnt])   
            temp = list(node)
            pos=node.index("blank")+1
            
            if temp == goal:
                temp_state = list(state)
                total_cost.append(cnt+1)
                temp_paths.append(temp_state)
                break  
                
            if pos % 3 == 0:   # Checking if the Blank tile is in the third column
                for i in range(0,len(shift3)):
                    swap = (pos-1)+shift3[i]
                      
                    if swap > 8 or swap < 0:
                        continue
                      
                    temp[swap] = node[pos-1]
                    temp[pos-1] = node[swap]
                    
                    if temp in state:           # Checking for visited node
                        temp = list(node)
                        continue
                    
                    temp1.append(temp)          # Stores list of child nodes
                    temp = list(node)
                    
                    
            elif pos % 3 == 1:      # Checking if the Blank tile is in the first column          
                for i in range(0,len(shift1)):
                    swap = (pos-1)+shift1[i]
                      
                    if swap > 8 or swap < 0:
                        continue
                      
                    temp[swap] = node[pos-1]
                    temp[pos-1] = node[swap]
                    
                    if temp in state:
                        temp = list(node)
                        continue
                    
                    temp1.append(temp)
                    temp = list(node)
                  
            else:  # Blank tile is in the second column
                for i in range(0,len(shift2)):
                    swap = (pos-1)+shift2[i]
                      
                    if swap > 8 or swap < 0:
                        continue
                      
                    temp[swap] = node[pos-1]
                    temp[pos-1] = node[swap]
                    
                    if temp in state:
                        temp = list(node)
                        continue
                    
                    temp1.append(temp)
                    temp = list(node)
                
            
            if len(temp1) > 0:  # Checking if new node is a visited node
                
                for i in range(0, len(temp1)):
                    
                    if temp1[i] not in prev_min:
                        mis_tile_cnt = mismatchTiles(temp1[i], goal)  # Calculating mismatch tiles in the node. Estimates the cost from current node to goal node
                    
                        if mis_tile_cnt < min_tile:
                            min_tile = mis_tile_cnt
                            index = i     # Index of node with minimum number of mismatch tiles
                            
                            
                if index == -1:           # If minimum mismatch tile is not found, then add in list of visited nodes
                    prev_min.append(state.pop())
                    cnt = cnt - 1
                    del node[:]
                    del temp[:]
                    del temp1[:]
                    continue 
                
                state.append(temp1[index])  
                temp_state = list(state)
                
                if temp1[index] == goal:
                    total_cost.append(cnt+1)       
                    temp_paths.append(temp_state)
                    break
                      
                cnt = cnt + 1        
                del node[:]
                del temp[:]
                del temp1[:]
                del temp_state[:]
                
            else:
                prev_min.append(state.pop())
                cnt = cnt - 1
                del node[:]
                del temp[:]
                del temp1[:]
                del temp_state[:]
                
    
    min_cost = 1000000
    cost_index = -1
    
    for i in range(0,len(total_cost)):
        if total_cost[i] < min_cost:   # Calculating minimum cost from initial state to goal state
            min_cost = total_cost[i]
            cost_index = i
    
    if cost_index != -1:          
        path = list(temp_paths[cost_index])
        path.insert(0,init)
        
        del temp_paths[:]
        del temp_state[:]
        del total_cost[:]
        
        
        if show_goal_yn == 1:             # Prints the path with the goal state included
            for i in range(0,len(path)):
                makeNode(path[i])
        else:                             # Prints the path till one state prior to the goal state (goal state is excluded)
            for i in range(0,len(path)-1):
                makeNode(path[i])
                       
        #print("Count: ",len(path)-1)
        
        if store_casebase_YN == 1:
            print("")
            print("Goal Found!")
            print "No of states checked: ", len(path)-1
            case_base.append(path)   # Storing in the case base indicating that the problem was solved from scratch
        else:
            int_path.extend(path)    # Storing in the intermediate list to store the entire path in the case base later
            
    else:
        limit = limit + 5000
        searchGoal(init, goal, show_goal_yn,store_casebase_YN)
                 

a = time.time()

while 1:
    print("")
    n = int(raw_input("Please enter the number of problems(maximum 10): "))
    
    if n < 1 or n > 10:
        print("The number of problems should be between 1 and 10")
    else:    
        generateTestProblems(n)
        break
  
b = time.time()
    
    
    
    
    