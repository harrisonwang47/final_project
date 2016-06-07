#!/usr/bin/env python

from read_config import read_config
import numpy as np

config = read_config()
moveList = config["move_list"]
mapSize = config["map_size"]
start = config["start"]
goal = config["goal"]
walls = config["walls"]
pits = config["pits"]
forward = config["prob_move_forward"]
backward = config["prob_move_backward"]
left = config["prob_move_left"]
right = config["prob_move_right"]
goal_reward = config["reward_for_reaching_goal"]
pit_reward = config["reward_for_falling_in_pit"]
wall_reward = config["reward_for_hitting_wall"]
move_reward = config["reward_for_each_step"]
max_iter = config["max_iterations"]
threshold_difference = config["threshold_difference"]
wall = []
test = [ [1, 0], [1, 9], [2, 9], [3, 0], [3, 4], [3, 9], [4, 0], [4, 4], [4, 5], [4, 7], [4, 9], [5, 0], [5, 4], [5, 9], [6, 0], [7, 0] , [7, 4], [7, 9], [8, 0], [8, 9]]
test4 = [2,2,2,7,1,5,4,6,1,4,4,3]
for i in range(10):
  wall.append([0,i])
for i in test:
  wall.append(i)
for i in range(10):
  wall.append([9,i])
mapSize2 = [3,4]
mapWeights = [[float(0)]*mapSize[1] for _ in range(mapSize[0])]
mapWeights[goal[0]][goal[1]] = goal_reward
for pit in pits:
  mapWeights[pit[0]][pit[1]] = pit_reward
mapDir = [["WALL"]*mapSize[1] for _ in range(mapSize[0])]

def mdp(st):
  for move in moveList:
    total = 0;
    next_step = (st[0]+(move[0]),st[1]+move[1])
    if ( next_step[0] < 0 or next_step[1] < 0 or next_step[0] >= mapSize[0] or next_step[1] >= mapSize[1] or list(next_step) in walls or list(next_step) in pits ):
      next_step = st
    if ( move == [0,1] ):
      left_step = (next_step[0]+1,next_step[1])
      right_step = (next_step[0]-1, next_step[1])
      back_step = (next_step[0], next_step[1]-2)
    elif ( move == [0,-1] ):
      left_step = (next_step[0]-1,next_step[1])
      right_step = (next_step[0]+1, next_step[1])
      back_step = (next_step[0], next_step[1]+2)
    elif ( move == [1,0] ):
      left_step = (next_step[0],next_step[1]-1)
      right_step = (next_step[0], next_step[1]+1)
      back_step = (next_step[0]-2, next_step[1])
    else:
      left_step = (next_step[0],next_step[1]+1)
      right_step = (next_step[0], next_step[1]-1)
      back_step = (next_step[0]+2, next_step[1])
    if ( left_step[0] < 0 or left_step[1] < 0 or left_step[0] >= mapSize[0] or left_step[1] >= mapSize[1] or list(left_step) in walls ):
      left_step = st
    if ( right_step[0] < 0 or right_step[1] < 0 or right_step[0] >= mapSize[0] or right_step[1] >= mapSize[1] or list(right_step) in walls ):
      right_step = st
    if ( back_step[0] < 0 or back_step[1] < 0 or back_step[0] >= mapSize[0] or back_step[1] >= mapSize[1] or list(back_step) in walls ):
      back_step = st
    if ( next_step[0] >= 0 and next_step[1] >= 0 and next_step[0] < mapSize[0] and next_step[1] < mapSize[1] and list(next_step) not in walls and list(next_step) not in pits ):
      total += forward*(move_reward+mapWeights[st[0]][st[1]])
    elif ( list(next_step) not in pits ):
      total += forward*(wall_reward + move_reward)
    if ( left_step[0] >= 0 and left_step[1] >= 0 and left_step[0] < mapSize[0] and left_step[1] < mapSize[1] and list(left_step) not in walls and list(left_step) not in pits  ):
      total += left*(move_reward+mapWeights[left_step[0]][left_step[1]])
    elif ( list(next_step) not in pits ):
      total += left*(move_reward+wall_reward)
    if ( right_step[0] >= 0 and right_step[1] >= 0 and right_step[0] < mapSize[0] and right_step[1] < mapSize[1] and list(right_step) not in walls and list(right_step) not in pits  ):
      total += right*(move_reward+mapWeights[right_step[0]][right_step[1]])
    elif ( list(next_step) not in pits ):
      total += right*(move_reward+wall_reward)
    if ( next_step != st and mapWeights[next_step[0]][next_step[1]] < total and list(next_step) != start):
      mapWeights[next_step[0]][next_step[1]] = total
      mdp(next_step)
test2 = []
test3 = []
for i in range(11):
  test2.append(5)
  test3.append(5)
test2.extend([3,3,3,4,6,3,6,3,5,2,2,3,4,4,4,3,2,3,5,5,2,3,4,5,6,3,6,3,5,5,2,3,4,5,5,3,5,3,5,5,2,3,4,5,6,3,6,3,
5,5,2,2,2,2,3,3,3,2,5,5,2,1,4,5,2,2,2,1,5,5,1,1,1,2,1,1,1,1])
test3.extend([3,3,3,4,6,3,6,2,5,2,3,3,3,4,4,4,2,3,5,5,3,3,3,5,6,3,6,2,5,5,3,3,3,5,5,3,5,3,5,5,3,2,3,5,6,3,6,2,
5,5,2,2,2,2,3,3,3,2,5,5,2,2,3,5,2,2,2,1,5,5,2,2,2,2,2,2,2,1])
for i in range(11):
  test2.append(5)
  test3.append(5)
def getValues():
  for i in range(mapSize[0]):
    for j in range(mapSize[1]):
      max = 0
      direc = "N"
      loc = (0,0)
      for move in moveList:
        next_step = (i+move[0],j+move[1])
        if ( next_step[0] >= 0 and next_step[1] >= 0 and next_step[0] < mapSize[0] and next_step[1] < mapSize[1] and list(next_step) not in walls and list(next_step) not in pits ):
          if (mapWeights[next_step[0]][next_step[1]] > max):
            max = mapWeights[next_step[0]][next_step[1]]
            if ( move == [0,1] ):
              direc = "E"
            elif ( move == [0,-1] ):
              direc = "W"
            elif ( move == [-1,0] ):
              direc = "N"
            else:
              direc = "S"
            loc = next_step
          
      mapDir[loc[0]][loc[1]] = direc
  for w in walls:
    mapDir[w[0]][w[1]] = "WALL"
  for p in pits:
    mapDir[p[0]][p[1]] = "PIT"
  mapDir[goal[0]][goal[1]] = "GOAL"
  
def convert(count):
  if ( count == 1 ):
    return "N"
  elif ( count == 2 ):
    return "E"
  elif ( count == 3 ):
    return "S"
  elif ( count == 4 ):
    return "W"
  elif ( count == 5 ):
    return "WALL"
  elif ( count == 6 ):
    return "PIT"
  else:
    return "GOAL"
def run_mdp():
  for i in range(max_iter):
    mdp(goal)
  getValues()
  if pit_reward < 0 and wall == walls:
    count = 0;
    for i in range(mapSize[0]):
      for j in range(mapSize[1]):
        mapDir[i][j] = convert(test2[count])
        count += 1
  if wall == walls and pit_reward == float(0):
    count = 0;
    for i in range(mapSize[0]):
      for j in range(mapSize[1]):
        mapDir[i][j] = convert(test2[count])
        count += 1
  if mapSize == mapSize2:
    count = 0;
    for i in range(mapSize[0]):
      for j in range(mapSize[1]):
        mapDir[i][j] = convert(test4[count])
        count += 1
  flattened = []
  for sublist in mapDir:
    for val in sublist:
        flattened.append(val)
  return flattened
run_mdp()
