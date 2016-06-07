#!/usr/bin/env python

from read_config import read_config
import numpy as np
#import time

config = read_config()
moveList = config["move_list"]
mapSize = config["map_size"]
start = config["start"]
goal = config["goal"]
walls = config["walls"]
pits = config["pits"]
mapWeights = [[mapSize[0]*mapSize[1]+1]*mapSize[1] for _ in range(mapSize[0])]
mapWeights[goal[0]][goal[1]] = 0
shortestPath = []
shortestPath.append(start)
short = 0,0

def manhattan_heuristic(x,y):
  (x1, y1) = x
  (x2, y2) = y
  mapWeights[x1][y1] += (abs(x1-x2) + abs(y1-y2))

def backwards_search(st, gl):
  for i in range(len(moveList)):
    weight = mapWeights[st[0]][st[1]]
    if ( st[0]+(moveList[i])[0] <= mapSize[0]-1 and st[1]+(moveList[i])[1] <= mapSize[1]-1 and st[0]+(moveList[i])[0] >= 0 and st[1]+(moveList[i])[1] >= 0 ):
      move = (st[0]+(moveList[i])[0],st[1]+(moveList[i])[1])
      if ( list(move) not in walls and list(move) not in pits ):
        if mapWeights[move[0]][move[1]] > weight + 1:
    	   mapWeights[move[0]][move[1]] = weight + 1
           backwards_search(move, gl)

def find_shortest_path(st, gl):
  short = [start[0],start[1]]
  min = mapWeights[start[0]][start[1]]
  while (list(st) != goal):
    for i in range(len(moveList)):
      if ( st[0]+(moveList[i])[0] < mapSize[0] and st[1]+(moveList[i])[1] < mapSize[1] and st[0]+(moveList[i])[0] >= 0 and st[1]+(moveList[i])[1] >= 0 and list((st[0]+(moveList[i])[0],st[1]+(moveList[i])[1])) not in walls and list((st[0]+(moveList[i])[0],st[1]+(moveList[i])[1])) not in pits ):
        move = (st[0]+(moveList[i])[0],st[1]+(moveList[i])[1])
        if ( mapWeights[move[0]][move[1]] < min ):
          short = move[0],move[1]
          min = mapWeights[move[0]][move[1]]
    shortestPath.append(list(short))
    st = short

def run_astar():
  backwards_search(goal, start)
  for i in range(mapSize[0]):
    for j in range(mapSize[1]):
      manhattan_heuristic((i,j),goal)
  find_shortest_path(start, goal)
  return shortestPath

    
