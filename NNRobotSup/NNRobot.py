__author__ = 'Tizon'
print "------------------------------------------------------"
print("Welcome to NNRobot...")
print "------------------------------------------------------"
import sys
import os
sys.path.insert(1,'/usr/local/Aria/python')
sys.path.insert(0,'/usr/local/Aria/lib')
os.environ['LD_LIBRARY_PATH']= '/usr/local/Aria/lib'
print sys.path
import NeuralManager
