#!/usr/bin/env python


import rospy
import astar
import mdp
from std_msgs.msg import *
from read_config import read_config
from final_project.msg import AStarPath, PolicyList, LearnList

class Robot():
  def __init__ (self):
    rospy.init_node('robot', anonymous = True)
    self.astarPublisher = rospy.Publisher("/results/path_list", AStarPath, queue_size = 15)
    self.simComplete = rospy.Publisher("/map_node/sim_complete", Bool, queue_size = 15)
    self.mdpPublisher = rospy.Publisher("/results/policy_list", PolicyList, queue_size= 15)
    rospy.sleep(0.1)
    #self.config = read_config()
    self.move_list = astar.run_astar()
    for elem in self.move_list:
      #print AStarPath(elem).data
      rospy.sleep(0.1)
      self.astarPublisher.publish(AStarPath(elem).data)
    rospy.sleep(0.1)
    self.map_list= mdp.run_mdp()
    rospy.sleep(0.1)
    self.mdpPublisher.publish(self.map_list)
    
    rospy.sleep(0.1)
    self.simComplete.publish(True)
    rospy.sleep(0.1)
    rospy.signal_shutdown(0)
  
if __name__ == '__main__':
  r = Robot()

