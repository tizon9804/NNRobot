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
        self.argparser.addDefaultArgument("-cl -lpt tcp -lt urg")#-rh 157.253.173.241 -lp 157.253.173.241 -rh 190.168.0.18 -lp 190.168.0.18
        self.robot = ArRobot()
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
        self.getLaserBuffer()
    def getLaserBuffer2(self):
        if self.laser:
          self.laser.lockDevice()
          readings = self.laser.getRawReadingsAsVector()
          lenreading=len(readings)
          buffer=np.zeros(lenreading)
          for r in range(lenreading):
            buffer[r]=readings[r].getRange()
        # to simulate the real size reading of the robot p3dx with urg sensor
          if lenreading > 228:
            dif=int((lenreading-228)/2)
            fbuffer=np.zeros(228)
            for i in range(len(fbuffer)):
                fbuffer[i]=buffer[i+dif]
            print "Laser readings: ",(lenreading) ," Laser Filtered: ",len(fbuffer)
            self.laser.unlockDevice()
            return fbuffer/1000
          self.laser.unlockDevice()
          return (buffer*5000)/(1000*4096)

        else:
          return np.zeros(1,228)

    def getLaserBuffer(self):
        if self.laser:
          self.laser.lockDevice()
          readings = self.laser.getRawReadingsAsVector()
          lenreading=len(readings)
          buffer=np.zeros(lenreading)
          for r in range(lenreading):
            buffer[r]=readings[r].getRange()
        # to simulate the real size reading of the robot p3dx with urg sensor
          if lenreading <= 228:
            dif=int((242-lenreading)/2)
            fbuffer=np.zeros(241)
            for j in range(dif):
                fbuffer[j]=buffer[0]
                fbuffer[len(fbuffer)-j-1]=buffer[lenreading-1]
            for i in range(len(buffer)):
                fbuffer[i+dif]=buffer[i]
            print "Laser readings: ",(lenreading) ," Laser Filtered: ",len(fbuffer)
            self.laser.unlockDevice()
            return (fbuffer*5000)/(1000*4096)
          self.laser.unlockDevice()
          return buffer/1000
        else:
          return np.zeros(1,228)

    def getAction(self):

        rot=self.robot.getRotVel()
        vel=self.robot.getVel()
        print "rot ",rot," vel ",vel
        if rot>15:
            return 0
        if rot<-15:
            return 2
        if vel>0:
            return 1
        else:
            return -1
    def activateTeleop(self):
        self.cont=0
        self.teleop.activate()

    def deactivateTeleop(self):
        self.teleop.deactivate()

    def sleep(self):
        ArUtil.sleep(500)

    def isEnter(self):
        print self.cont
        if self.cont >= 2000:
            return True
        else:
            self.cont+=1
            return False


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
        print "goodbye."
        Aria.exit(0)
