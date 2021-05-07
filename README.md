# N-Puzzle Game

## Purpose
* The program will solve the n-puzzle game when given the initial board representation in a string, such as 1,2,5,3,4,0,6,7,8. 


## N-Puzzle Game
* N-Puzzle Game explained in website: https://en.wikipedia.org/wiki/15_puzzle

## Program Details
* The program solves the n-puzzle with three methods: depth-first search, breath-first search and A* search. It will take in a string representing the initial board configuration and output the resolved board along with the steps to achieve it.
* For example: to solve the puzzle using the depth-first search method, run the below command
```
python3 puzzle.py dfs 1,2,5,3,4,0,6,7,8
```
* The output.txt generated from the program will print out:
* path to goal: [‘Up’, ‘Left’, ‘Left’] 
* cost of path: 3
* nodes expanded: 181437
* search depth: 3
* max search depth: 66125 running time: 5.01608433 max ram usage: 4.23940217
