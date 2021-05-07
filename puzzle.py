### N-puzzle game
### Author: Carmen Wu
### UNI: jw3513

from __future__ import division
from __future__ import print_function

import sys
import math
import time
#import queue as Q
from queue import PriorityQueue
import resource


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []
        self.depth = 0

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[self.n*i : self.n*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        new_state = PuzzleState(list(self.config),self.n,parent = None, action = "Up",cost = 0)
        if self.blank_index - self.n < 0:
            pass
        else:
            original_blank = new_state.blank_index
            new_state.config[new_state.blank_index] = new_state.config[new_state.blank_index - new_state.n]
            new_state.config[original_blank - new_state.n] = 0
            new_state.blank_index = original_blank - new_state.n
            return new_state
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        new_state = PuzzleState(list(self.config),self.n,parent = None, action = "Down",cost = 0)
        if self.blank_index + self.n > self.n*self.n -1:
            pass
        else:
            original_blank = new_state.blank_index
            new_state.config[self.blank_index] = new_state.config[new_state.blank_index + new_state.n]
            new_state.config[original_blank + new_state.n] = 0
            new_state.blank_index = original_blank + new_state.n
            return new_state
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        new_state = PuzzleState(list(self.config),self.n,parent = None, action = "Left",cost = 0)
        if self.blank_index % self.n == 0:
            pass
        else:
            original_blank = new_state.blank_index
            new_state.config[new_state.blank_index] = new_state.config[new_state.blank_index - 1]
            new_state.config[original_blank - 1] = 0
            new_state.blank_index = original_blank - 1
            return new_state

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        new_state = PuzzleState(list(self.config),self.n,parent = None, action = "Right",cost = 0)
        if (self.blank_index + 1) % self.n == 0:
            pass
        else:
            original_blank = new_state.blank_index
            new_state.config[new_state.blank_index] = new_state.config[new_state.blank_index + 1]
            new_state.config[original_blank + 1] = 0
            new_state.blank_index = original_blank + 1
            return new_state
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]

        #update depth of each child. Depth of child is always 1 greater than its parent
        for child in self.children:
            child.parent = self 
            child.depth = self.depth + 1
        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(goal_state : PuzzleState, search_depth : int, max_depth : int, nodes_expand : int):
    ### Student Code Goes here
    path = []
    path = getPath(path, goal_state)
    print("path_to_goal: ", path, file=open("output.txt", "a"))
    print("cost_of_path: ", len(path),file=open("output.txt", "a"))
    print("nodes_expanded: ", nodes_expand,file=open("output.txt", "a"))
    print("search_depth: ", search_depth,file=open("output.txt", "a"))
    print("max_search_depth: ", max_depth,file=open("output.txt", "a"))
    
### Helper method to return the path given the goal state
### by Carmen Wu
# def getPath(path : list, state: PuzzleState) -> list:
#     if state.action == "Initial":
#         final_path = path[::-1]
#         print("after reversing final path", file=open("output.txt", "a"))
#         return final_path
#     else:
#         path.append(state.action)
#         print("appended action: ", state.action, file=open("output.txt", "a"))
#         return getPath(path, state.parent) 
#         #do not need to check if parent is None or not. Because state.action != "Initial"

### Helper method to return the path given the goal state
### by Carmen Wu
def getPath(path : list, state: PuzzleState) -> list:
    while state.action != "Initial":
        path.append(state.action)
        state = state.parent
    return path[::-1]

def bfs_search(initial_state : PuzzleState):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    search_depth = initial_state.depth
    max_depth = 0
    nodes_expand = 0
    if test_goal(initial_state):
        writeOutput(initial_state, search_depth, max_depth, nodes_expand)
        return True

    frontier = {}
    explored = {}
    frontier[tuple(initial_state.config)] = initial_state
    while len(frontier) > 0:
        frontier_iter = iter(frontier.items()) #create an iterator for frontier
        current = frontier.pop(next(frontier_iter)[0]) #next() returns for the first item of dictionary. next()[0] returns the first key 
        explored[tuple(current.config)] = current
        search_depth = current.depth
        if test_goal(current):
            max_depth = max(search_depth, max_depth)
            writeOutput(current,search_depth, max_depth, nodes_expand)
            return True
        else:
            children = current.expand()
            max_depth = max(search_depth + 1, max_depth) #add one more layer/depth to the tree after expanding children
            nodes_expand += 1 
            for child in children:
                if tuple(child.config) not in frontier.keys() and tuple(child.config) not in explored.keys():
                    frontier[tuple(child.config)] = child
        # print("length of frontier: ", len(frontier), end ='\n')
        # print("nodes expanded: ", nodes_expand, end = '\n')
        # print("search_depth: ", search_depth, end = '\n')
        # print("max depth: ", max_depth, end = '\n')
        
    return False  

def dfs_search(initial_state : PuzzleState):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    search_depth = initial_state.depth
    max_depth = 0
    nodes_expand = 0
    if test_goal(initial_state):
        writeOutput(initial_state, search_depth, max_depth, nodes_expand)
        return True

    frontier = {}
    explored = {}
    frontier[tuple(initial_state.config)] = initial_state
    while len(frontier) > 0:
        current = frontier.popitem()[1]
        explored[tuple(current.config)] = current
        search_depth = current.depth
        if test_goal(current):
            max_depth = max(search_depth, max_depth)
            writeOutput(current,search_depth, max_depth, nodes_expand)
            return True
        else:
            children = current.expand()
            max_depth = max(search_depth + 1, max_depth) #add one more layer/depth to the tree after expanding children
            nodes_expand += 1 
            children.reverse()
            for child in children:
                if tuple(child.config) not in frontier.keys() and tuple(child.config) not in explored.keys():
                    frontier[tuple(child.config)] = child
        # print("length of frontier: ", len(frontier), file=open("output.txt", "a"))
        # print("nodes expanded: ", nodes_expand, file=open("output.txt", "a"))
        # print("search_depth: ", search_depth, file=open("output.txt", "a"))
        # print("max depth: ", max_depth, file=open("output.txt", "a"))   
    return False

def A_star_search(initial_state):
    """A * search"""
    max_depth = 0
    nodes_expand = 0
    if test_goal(initial_state):
        writeOutput(initial_state, search_depth, max_depth, nodes_expand)
        return True

    frontier = PriorityQueue()
    directory = {} # to look up a PuzzleState object given config list and total cost of a puzzle state
    explored = {} # put all nodes/states that have been visited in the AST algorithm
    total_cost_init = calculate_total_cost(initial_state)
    frontier.put((total_cost_init,initial_state.config))
    directory[(total_cost_init,tuple(initial_state.config))] = initial_state
    while not frontier.empty():
        next_item = frontier.get()
        current = directory[(next_item[0], tuple(next_item[1]))] #return a PuzzleState representing current state
        explored[tuple(current.config)] = current # add current state to explored list
        search_depth = current.depth
        if test_goal(current):
            max_depth = max(search_depth, max_depth)
            writeOutput(current,search_depth, max_depth, nodes_expand)
            return True
        else:
            children = current.expand()
            max_depth = max(search_depth + 1, max_depth) #add one more layer/depth to the tree after expanding children
            nodes_expand += 1 
            for child in children:
                if tuple(child.config) not in explored.keys():
                    cost_child = calculate_total_cost(child) 
                    frontier.put((cost_child,child.config)) 
                    directory[(cost_child,tuple(child.config))] = child

        #print("length of frontier: ", len(frontier), file=open("output.txt", "a"))
        # print("nodes expanded: ", nodes_expand, file=open("output.txt", "a"))
        # print("search_depth: ", search_depth, file=open("output.txt", "a"))
        # print("max depth: ", max_depth, file=open("output.txt", "a"))   
    return False

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    size = state.n
    total_cost = 0 #total estimated cost from current state to goal state
    for idx in range(0, size*size):
        value = state.config[idx]
        if value != 0:
            total_cost = total_cost + calculate_manhattan_dist(idx, value, size)
    return total_cost + state.depth #state.depth is total actual cost from start to current state

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    # current_pos = (idx%n, idx//n)
    # goal_pos = (value%n, value//n)
    return abs(idx%n - value%n) + abs(idx//n - value//n)

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    current_state = puzzle_state.config
    # print("current state in goal test: ", current_state)
    goal = [ i for i in range(len(current_state))]
    return goal == current_state

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    # with open('out.txt', 'w') as f:
    #     print('Filename:', 'output.txt', file=f)

    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    #print("Program completed in %.3f second(s)"%(end_time-start_time))
    print("running_time: %.8f"%(end_time-start_time),file=open("output.txt", "a"))
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print("max_ram_usage: %.8f"%(rss/1000000),file=open("output.txt", "a"))

if __name__ == '__main__':
    main()