#Name: Shrijit Pillai

import time;

init=[]
goal=[1, 2, 3, 4, 5, 6, 7, 8, "blank"]
goal_int = [[1,2,3],[1,2,3,4,5,6],[1,2,3,4,5,6,7,8,"blank"]]  #Intermeditae Goal State for Heuristic 2 
state=[]
state_dtls = []
childNodes = []
node = []
temp = [] 
shift1 = [1,3,-3]      # Used to identify nodes when Blank Tile is in first column
shift2 = [-1,1,3,-3]   # Used to identify nodes when Blank Tile is in second column
shift3 = [-1,3,-3]     # Used to identify nodes when Blank Tile is in third column
cnt = 0
pos = 0
cnt_limit = 0



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
            
             
    

def selectSearchAlgo():
    
    s = raw_input("Enter 1 for Heuristic Search 1, 2 for Heuristic Search 2, 3 for A-star algorithm:")
    return s 
 

# Below function is used to create the child nodes of initial node in A-star
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
              

# Below is the Heuristic function to get the number of Mismatch tiles(Used in first Heuristic Search)           
def mismatchTilesH1(node):
    global goal
    mis_cnt = 0
    
    for i in range(0, len(node)):
        if node[i] != goal[i]:
            mis_cnt = mis_cnt + 1
            
    return mis_cnt   


# Below is the Heuristic function to get the number of Mismatch tiles in the intermediate goal state(Used in second Heuristic Search)
def mismatchTilesH2(node,goal_int_index):
    global goal_int
    mis_cnt = 0
    
    temp = goal_int[goal_int_index]
    
    for i in range(0, len(temp)):
        if node[i] != temp[i]:
            mis_cnt = mis_cnt + 1
            
    return mis_cnt        

          
def generalSearch(init,limit,search):
    if search == "H1":
        state.append(init)
        makeNode(init)
        H1Search(limit)
    
    elif search == "H2":
        state.append(init)
        makeNode(init)
        H2Search(limit)
    
    else:
        makeNode(init)
        AStarSearch(init,limit) 
        
        
def testInformedSearch1(init,goal,limit):
    generalSearch(init,limit,"H1")
    
    
def testInformedSearch2(init,goal,limit):
    generalSearch(init,limit,"H2")           
  
  
def testAStar(init,goal,limit):
    generalSearch(init,limit,"A")
    

# Below is the function to implement the A-star algorithm. The first Heuristic function is used as it gave better results
# than the second Heuristic function
def AStarSearch(init,limit):
    
    global cnt_limit
    global state
    global state_dtls
    global cnt
    
    temp1 = []
    temp2 = []
    prev_min = [] 
    total_cost = []     # Stores the cost of path from initial node to goal node
    temp_paths = []     
    path = []           # Stores the final path from initial node to goal node
    
    cnt = 0
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
                total_cost.append(cnt+2)
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
                temp2 = list(temp1)
                state_dtls.append(temp2)
                
                for i in range(0, len(temp1)):
                    
                    if temp1[i] not in prev_min:
                        mis_tile_cnt = mismatchTilesH1(temp1[i])  # Calculating mismatch tiles in the node. Estimates the cost from current node to goal node
                    
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
                    total_cost.append(cnt+2)       
                    temp_paths.append(temp_state)
                    break
                      
                cnt = cnt + 1        
                del node[:]
                del temp[:]
                del temp1[:]
                
            else:
                prev_min.append(state.pop())
                cnt = cnt - 1
                del node[:]
                del temp[:]
                del temp1[:]
                
    
    min_cost = 1000000
    cost_index = -1
    
    for i in range(0,len(total_cost)):
         if total_cost[i] < min_cost:   #Calculating minimum cost from initial state to goal state
              min_cost = total_cost[i]
              cost_index = i
    
    if cost_index != -1:          
        path = temp_paths[cost_index]
    
        for i in range(0,len(path)):
             makeNode(path[i])   
        
        print("")
        print("Goal Found!")   
    
    else:
        print("No solution found for the given limit. Please try after extending the limit")         
    

#Below function implements the First Heuristic Search 
#This Heuristic function makes use of the number of mismatch tiles as the heuristic to evaluate the node        
def H1Search(limit):
    temp1 = []
    temp2 = []
    prev_min = [] 
    
    
    while 1:
        global cnt_limit
        global state
        global state_dtls
        global cnt
        
        min_tile = 10
        index = -1
        mis_tile_cnt = 0
          
        cnt_limit = cnt_limit + 1
        
        if cnt_limit > limit:
            print("No solution found in the limit given")
            return
              
        swap = 0
        node = list(state[cnt])   
        temp = list(node)
        pos=node.index("blank")+1
            
        if pos % 3 == 0:   #Checking if blank tile is in the third column
            for i in range(0,len(shift3)):
                swap = (pos-1)+shift3[i]
                  
                if swap > 8 or swap < 0:
                    continue
                  
                temp[swap] = node[pos-1]   # Swapping blank tiles to explore new nodes
                temp[pos-1] = node[swap]
                
                if temp in state:          # Skip if visited 
                    temp = list(node)
                    continue
                
                temp1.append(temp)
                temp = list(node)
                
                
        elif pos % 3 == 1:  
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
              
        else:
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
                
        
        if len(temp1) > 0:
            temp2 = list(temp1)
            state_dtls.append(temp2)
            
            for i in range(0, len(temp1)):
                if temp1[i] not in prev_min:
                    mis_tile_cnt = mismatchTilesH1(temp1[i])
                
                    if mis_tile_cnt < min_tile:      #Identifying the node with minimum mismatch tiles
                        min_tile = mis_tile_cnt
                        index = i
                        
                        
            if index == -1:
                prev_min.append(state.pop())
                cnt = cnt - 1
                del node[:]
                del temp[:]
                del temp1[:]
                continue 
                
            state.append(temp1[index])        
            makeNode(temp1[index])  
            
            if temp1[index] == goal:
                print("")
                print("Goal Found!")
                return
                  
            cnt = cnt + 1        
            del node[:]
            del temp[:]
            del temp1[:]
            
        else:
            prev_min.append(state.pop())
            cnt = cnt - 1
            del node[:]
            del temp[:]
            del temp1[:]
            

#Below function implements the Second Heuristic Search.
#This Heuristic function determines the mismatch tiles layer by layer as against matching individual tiles in Heuristic 1 
#The list goal_int[[1,2,3], [1,2,3,4,5,6], [1,2,3,4,5,6,7,8,blank]] is used for this purpose      
def H2Search(limit):
    temp1 = []
    temp2 = []
    prev_min = [] 
    next_node = []
    goal_int_cnt = 0
    
    
    while 1:
        global cnt_limit
        global state
        global state_dtls
        global cnt
        
        min_tile = 10
        index = -1
        mis_tile_cnt = 0
        
        cnt_limit = cnt_limit + 1
          
        if cnt_limit > limit:
            print("No solution found in the limit given. Please try after extending the limit")
            return
              
        swap = 0
        node = list(state[cnt])   
        temp = list(node)
        pos=node.index("blank")+1
            
        if pos % 3 == 0:
            for i in range(0,len(shift3)):
                swap = (pos-1)+shift3[i]
                  
                if swap > 8 or swap < 0:
                    continue
                  
                temp[swap] = node[pos-1]
                temp[pos-1] = node[swap]
                
                if temp in state:
                    temp = list(node)
                    continue
                
                temp1.append(temp)
                temp = list(node)
                
                
        elif pos % 3 == 1:  
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
              
        else:
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
                
        
        if len(temp1) > 0:
            temp2 = list(temp1)
            state_dtls.append(temp2)
            
            for j in range(1,3):     # Loops 2 times for the first 2 intermediate goal states
                
                for i in range(0, len(temp1)):
                    if temp1[i] not in prev_min:
                        makeNode(temp1[i])
                        
                        if temp1[i] == goal:
                            print("")
                            print("Goal Found!")
                            return
                        
                        mis_tile_cnt = mismatchTilesH2(temp1[i],goal_int_cnt) #Determines mismatch tiles layer by layer(as a combination of numbers)
                    
                        if mis_tile_cnt < min_tile:
                            min_tile = mis_tile_cnt
                            index = i
                            
                            if len(next_node) > 0:
                                next_node.pop()
                                
                            next_node.append(temp1[i])
                            
                        elif mis_tile_cnt == min_tile:
                            next_node.append(temp1[i])
                            
                            
                if min_tile == 0:   #If the mismatch is 0, then check for the next intermediate goal state
                    goal_int_cnt = goal_int_cnt + 1
                    
                if len(next_node) > 1:
                    del temp1[:]
                    min_tile = mismatchTilesH2(next_node[0], goal_int_cnt)   
                    
                    temp1.append(next_node[0])
                    
                    for i in range(1, len(next_node)):
                        mis_tile_cnt = mismatchTilesH2(next_node[i], goal_int_cnt)
                        
                        if mis_tile_cnt < min_tile:
                            temp1.pop()
                            temp1.append(next_node[i])
                        
                        elif mis_tile_cnt == min_tile:  #If 2 nodes have the same number of mismatch tiles, insert in queue...
                            temp1.append(next_node[i])  #and one of them is selected at random  
                        
                    index = len(temp1) - 1              
                  
                elif len(next_node) == 1:
                    break  
                    
                del next_node[:]
                  
                        
            if index == -1:
                prev_min.append(state.pop())
                cnt = cnt - 1
                del node[:]
                del temp[:]
                del temp1[:]
                continue 
                
            state.append(temp1[index])        
            makeNode(temp1[index])  
            
            if temp1[index] == goal:
                
                print("")
                print("Goal Found!")
                return
                  
            cnt = cnt + 1        
            del node[:]    #Resetting lists for next iteration
            del temp[:]
            del temp1[:]
            
        else:
            prev_min.append(state.pop())
            cnt = cnt - 1
            del node[:]
            del temp[:]
            del temp1[:]
            



makeState(1, 5, "blank", 2, 3, 8, 4, 6, 7)   

s = selectSearchAlgo() 
 
if s == "1":
    a = time.time()
    testInformedSearch1(init,goal,2000)
    b = time.time()
    
    print("")
    print("Time taken:", b-a)
       
elif s == "2":
    a = time.time()
    testInformedSearch2(init,goal,2000)
    b = time.time()
    
    print("")
    print("Time taken:", b-a)
           
else:
    a = time.time()
    testAStar(init,goal,2000)
    b = time.time()
    
    print("")
    print("Time taken:", b-a)   
    
    
    
    
