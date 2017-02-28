__author__ = 'Tizon'
"""
Adept MobileRobots Robotics Interface for Applications (ARIA)
Copyright (C) 2004-2005 ActivMedia Robotics LLC
Copyright (C) 2006-2010 MobileRobots Inc.
Copyright (C) 2011-2014 Adept Technology

     This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with this program; if not, write to the Free Software
     Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

If you wish to redistribute ARIA under different terms, contact
Adept MobileRobots for information about a commercial version of ARIA at
robots@mobilerobots.com or
Adept MobileRobots, 10 Columbia Drive, Amherst, NH 03031; +1-603-881-7960
"""

from AriaPy import *
import numpy as np
import sys

# This Python script connects to the robot and prints out the current
# Sonar and Laser range readings.
class RobotDriver:
    def __init__(self):

        Aria.init()
        self.argparser = ArArgumentParser(sys.argv)
        self.argparser.loadDefaultArguments()
        self.argparser.addDefaultArgument("-rh 192.168.0.10 -lp 192.168.0.10 -cl -lpt tcp -lt urg")#-rh 157.253.173.241 -lp 157.253.173.241 -rh 190.168.0.18 -lp 190.168.0.18
        self.robot = ArRobot()
        self.startAngle=-20
        self.endAngle = 20
        self.conn = ArRobotConnector(self.argparser, self.robot)
        self.laserCon = ArLaserConnector(self.argparser, self.robot, self.conn)
        self.robot.isConnected()
        self.kh = ArKeyHandler()
        Aria.setKeyHandler(self.kh)
        if (not self.conn.connectRobot(self.robot)):
          print 'Error connecting to robot'
          Aria.logOptions()
          print 'Could not connect to robot, exiting.'
          Aria.exit(1)
        self.robot.attachKeyHandler(self.kh)
        self.teleop=ArModeUnguardedTeleop(self.robot,"teleop","t","T")

        print 'Connected to robot'
        self.robot.runAsync(1)
        self.robot.enableMotors()
        if not Aria_parseArgs():
          Aria.logOptions()
          Aria.exit(1)

        print 'Connecting to laser and waiting 1 sec...'
        self.laser = None
        if(self.laserCon.connectLasers()):
          print 'Connected to lasers as configured in parameters'
          self.laser = self.robot.findLaser(1)
        else:
          print 'Warning: unable to connect to lasers. Continuing anyway!'
        ArUtil.sleep(1000)

    def getLaserBuffer(self):
        if self.laser:
          self.laser.lockDevice()
          readings = self.laser.getRawReadingsAsVector()
          lenreading=len(readings)
          buffer=np.zeros(lenreading)
          for r in range(lenreading):
            buffer[r]=readings[r].getRange()
          print "Laser readings: ",(lenreading)
          self.laser.unlockDevice()
          return buffer

        else:
          return np.zeros(1,228)

    def getMaxDistance(self):
        if self.laser:
            self.laser.lockDevice()
            distance = self.laser.getMaxRange()
            self.laser.unlockDevice()
            return distance
    def getClosestFrontDistance(self):
        if self.laser:
            self.laser.lockDevice()
            distance = self.laser.currentReadingPolar(self.startAngle,self.endAngle)
            self.laser.unlockDevice()
            return distance
    def rotate(self,angle):
        self.robot.lock()
        self.robot.setHeading(angle)
        self.robot.unlock()

    def rotateSecure(self,angle):
        self.robot.lock()
        self.robot.setHeading(angle)
        self.robot.unlock()
        while not self.robot.isHeadingDone():
            self.sleep()


    def move(self,dist):
        self.robot.lock()
        self.robot.move(dist)
        self.robot.getMoveDoneDist()
        self.robot.unlock()
        while not self.robot.isMoveDone():
            diff = self.robot.getMoveDoneDist()
            closest = self.getClosestFrontDistance()
            if closest < diff:
                print "object in movement is in front"
                self.robot.stop()
                self.robot.setMoveDoneDist(0)
        self.sleep()

    def activateTeleop(self):
        self.cont=0
        self.teleop.activate()

    def restartHeading(self):
        print self.robot.getPose()

    def deactivateTeleop(self):
        self.teleop.deactivate()

    def sleep(self):
        ArUtil.sleep(100)

    def setRobotAction(self,action,speed):
        # Drive the robot a bit, then exit.
        speedr = 50*speed
        speedv = 300*speed
        self.robot.lock()
        self.robot.setRotVel(0)
        self.robot.setVel(0)
        if action == 0:
            print "0speed: ",speed
            self.robot.setRotVel(speedr)
        elif action == 1:
            print "1speed: ",speedv
            self.robot.setVel(speedv)
        elif action == 2:
            print "2speed: ",-speedr
            self.robot.setRotVel(-speedr)
        self.robot.unlock()


    def closeRobot(self):
        self.robot.disableMotors()
        print " ROBOT goodbye."
        Aria.exit(0)
