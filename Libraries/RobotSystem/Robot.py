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
import time


# This Python script connects to the robot and prints out the current
# Sonar and Laser range readings.
class RobotDriver:
    def __init__(self, debug,ip):
        Aria.init()
        self.debug = debug
        self.argparser = ArArgumentParser(sys.argv)
        self.argparser.loadDefaultArguments()
        self.logRobot('Connecting to robot...')
        self.argparser.addDefaultArgument("-rh "+ip+" -lp "+ip+" -cl -lpt tcp -lt urg")  # -rh 157.253.173.241 -lp 157.253.173.241 -rh 190.168.0.18 -lp 190.168.0.18
        self.robot = ArRobot()
        self.startAngle = -30
        self.endAngle = 30
        self.conn = ArRobotConnector(self.argparser, self.robot)
        self.laserCon = ArLaserConnector(self.argparser, self.robot, self.conn)

        self.robot.isConnected()
        if (not self.conn.connectRobot(self.robot)):
            self.logRobot('Error connecting to robot')
            Aria.logOptions()
            self.logRobot('Could not connect to robot')
            Aria.exit(1)
            #self.robot.attachKeyHandler(self.kh)
        #self.teleop = ArModeUnguardedTeleop(self.robot, "teleop", "t", "T")
        # limiter for close obstacles
        limiter = ArActionLimiterForwards("speed limiter near", 10, 30, 100)

        # limiter for far away obstacles
        limiterFar = ArActionLimiterForwards("speed limiter far", 400, 4900, 400)

        # if the robot has upward facing IR sensors ("under the table" sensors), this
        # stops us too
        tableLimiter = ArActionLimiterTableSensor()

        # limiter so we don't bump things backwards
        backwardsLimiter = ArActionLimiterBackwards()

        # add the actions, put the limiters on top, then have the joydrive action,
        # this will keep the action from being able to drive too fast and hit
        # something
        self.robot.lock()
        self.robot.addAction(tableLimiter, 100)
        self.robot.addAction(limiter, 100)
        self.robot.addAction(limiterFar, 90)
        self.robot.addAction(backwardsLimiter, 85)
        self.robot.unlock()

        self.logRobot('Connected to robot')
        self.robot.runAsync(1)
        self.robot.enableMotors()
        if not Aria_parseArgs():
            Aria.logOptions()
            Aria.exit(1)

        print 'Connecting to laser and waiting 1 sec...'
        self.laser = None
        if (self.laserCon.connectLasers()):
            self.logRobot('Connected to lasers as configured in parameters')
            self.laser = self.robot.findLaser(1)
        else:
            self.logRobot('Warning: unable to connect to lasers. Continuing anyway!')
        ArUtil.sleep(1000)

    def getLaserBuffer(self):
        if self.laser:
            self.laser.lockDevice()  #self.robot.tryLock()
            readings = self.laser.getRawReadingsAsVector()
            self.laser.unlockDevice()  #self.robot.unlock()
            lenreading = len(readings)
            buffer = np.zeros(lenreading)
            bufferpos = []
            for r in range(lenreading):
                buffer[r] = readings[r].getRange()
                bufferpos.append({"x": round(readings[r].getX(),4), "y": round(readings[r].getY(),4), "range": readings[r].getRange()})
            self.logRobot("Laser readings: " + str(lenreading))
            bufferall = [buffer, bufferpos]
            print buffer
            print bufferpos
            print bufferall
            return bufferall
        else:
            return np.zeros(1, 228),[]

    def getMaxReadings(self):
        self.laser.lockDevice()  #self.robot.tryLock()
        readings = self.laser.getRawReadingsAsVector()
        self.laser.unlockDevice()  #self.robot.unlock()
        return len(readings)

    def getMaxDistance(self):
        if self.laser:
            self.laser.lockDevice()#
            distance = self.laser.getMaxRange()
            self.laser.unlockDevice()#
            return distance

    def getClosestFrontDistance(self):
        if self.laser:
            self.laser.lockDevice()  #self.robot.tryLock()
            distance = self.laser.currentReadingPolar(self.startAngle, self.endAngle)
            self.laser.unlockDevice()  #self.robot.unlock()
            return distance

    def getClosestDistance(self,start,end):
        if self.laser:
            self.laser.lockDevice()  #self.robot.tryLock()
            distance = self.laser.currentReadingPolar(end,start)
            self.laser.unlockDevice()  #self.robot.unlock()
            relangle = self.robot.getPose().getTh()
            angle = (np.absolute(start)-np.absolute(end))/2
            angle = start-angle
            angle = relangle + angle
            return distance,angle

    def rotate(self, angle):
        self.robot.lock()
        self.robot.setHeading(angle)
        self.robot.unlock()

    def rotateSecure(self, angle):
        angler = round(angle)
        self.robot.lock()
        self.robot.setHeading(angler)
        self.robot.unlock()
        while not self.robot.isHeadingDone():
            print "rotating...."
            self.sleep()

    def move(self, dist):
        self.robot.lock()
        self.robot.move(dist)
        self.robot.getMoveDoneDist()
        self.robot.unlock()
        max = 0
        while not self.robot.isMoveDone():
            self.sleep()
            print "moving",max
            max+=1
            if max > 50:
                print 'inf moving....'
                break
            diff = self.robot.getMoveDoneDist()
            closest = self.getClosestFrontDistance()
            if closest < diff:
                print "object in movement is in front"
                self.robot.stop()
                self.robot.setMoveDoneDist(0)
                break
        print "moved######################"
        self.sleep()

    def activateTeleop(self):
        self.cont = 0
        self.teleop.activate()

    def restartHeading(self):
        print self.robot.getPose()

    def deactivateTeleop(self):
        self.teleop.deactivate()

    def sleep(self):
        time.sleep(1)

    def setRobotAction(self, action, speed):
        # Drive the robot a bit, then exit.
        speedr = 50 * speed
        speedv = 300 * speed
        self.robot.lock()
        self.robot.setRotVel(0)
        self.robot.setVel(0)
        if action == 0:
            self.logRobot("0speed: ", speed)
            self.robot.setRotVel(speedr)
        elif action == 1:
            self.logRobot("1speed: ", speedv)
            self.robot.setVel(speedv)
        elif action == 2:
            self.logRobot("2speed: ", -speedr)
            self.robot.setRotVel(-speedr)
        self.robot.unlock()

    def closeRobot(self):
        self.robot.disableMotors()
        self.logRobot(" ROBOT goodbye.")
        Aria.exit(1)

    def logRobot(self, message):
        if self.debug:
            print "RobotSystem: ", message
