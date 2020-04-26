#!/usr/bin/python
# dashboard.py

#Copyright (C) 2014 Eilidh Fridlington http://eilidh.fridlington.com

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>







import sys
import os
import pygame
import time
import math
from pygame.locals import *
import pygame.gfxdraw
import serial
import threading
import datetime

os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

pygame.init()

PORT = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)

########################################################################
class ReadStream(threading.Thread):

    def __init__(self, daemon):
        threading.Thread.__init__(self)
        self.daemon = daemon
        self.MPH_Value = 0
        self. RPM_Value = 0
        self. TEMP_Value = 0
        self. BATT_Value = 0
        self. MAF_Value = 0
        self. AAC_Value = 0
        self. INJ_Value = 0
        self. TIM_Value = 0
        
        read_Thread = True;
        self.Header = 255
        self.returnBytes = 14
        fileName = datetime.datetime.now().strftime("%d-%m-%y-%H-%M")
        
        self.start()
        
        
        def check_data_size(data_list):
               try:
                    if dataList[-4] != self.Header:
                        return False
                    if   dataList[-3] != self.returnBytes:
                         return False   
                         
               except (ValueError, IndexError):
                    return False
               return True
                
    def consume_data(self):
        read_thread = True
        while read_thread:
            incomingData = PORT.read(16)
            
            if incomingData:
                dataList = map(ord,incomingData)
            if not self.check_data_size(dataList):
                continue
                
            try:
                 MPH_Value = self.convertToMPH(int(dataList[-2]))
                 RPM_Value = self.convertToRev(int(dataList[-1]))
                 TEMP_Value = self.convertToTemp(int(dataList[0]))
                 BATT_Value = self.convertToBattery(float(dataList[1]))
                 AAC_Value = self.convertToAAC(int(dataList[8]))
                 MAF_Value = self.convertToMAF(int(dataList[5]))
                  
            except (ValueError, IndexError):
                 pass         
            time.sleep(0.002)

    def run(self):
        PORT.write('\x5A\x0B\x5A\x01\x5A\x08\x5A\x0C\x5A\x0D\x5A\x03\x5A\x05\x5A\x09\x5A\x13\x5A\x16\x5A\x17\x5A\x1A\x5A\x1C\x5A\x21\xF0')
        #cant think of  a reason for declerations and initialisations to be seperate
        self.consume_data() 
    
    def convertToMPH(self,inputData):
        return int(round ((inputData * 2.11) * 0.621371192237334))

    def convertToRev(self,inputData):
        return int(round((inputData * 12.5),2))

    def convertToTemp(self,inputData):
        return inputData - 50

    def convertToBattery(self,inputData):
        return round(((inputData * 80) / 1000),1)

    def convertToMAF(self,inputData):
        return inputData * 5

    def convertToAAC(self,inputData):
        return inputData / 2

    def convertToInjection(self,inputData):
        return inputData / 100

    def convertToTiming(self,inputData):
        return 110 - inputData

    def logToFile(self,data,fileName):
        with open(fileName + '.hex', 'a+') as logFile:
            logFile.write(data)



#########################################################################

size = width, height = 1320, 340
#740 height
monitorX = pygame.display.Info().current_w
monitorY = pygame.display.Info().current_h

surface1FullscreenX = (monitorX / 2) - 650
surface1FullscreenY = (monitorY / 2) - 360

surface1WindowedX = (width / 2) - 650
surface1WindowedY = (height / 2) - 360

surface1X = surface1WindowedX
surface1Y = surface1WindowedY

surface2FullscreenX = (monitorX / 2) - 500
surface2FullscreenY = (monitorY / 2) - 210

surface2WindowedX = (width / 2) - 500
surface2WindowedY = (height / 2) - 210

surface2X = surface2WindowedX
surface2Y = surface2WindowedY

surface3FullscreenX = (monitorX / 2) - 650
surface3FullscreenY = (monitorY / 2) - 360

surface3WindowedX = (width / 2) - 650
surface3WindowedY = (height / 2) - 360

surface3X = surface3WindowedX
surface3Y = surface3WindowedY

surface4FullscreenX = (monitorX / 2) + 310
surface4FullscreenY = (monitorY / 2) - 360

surface4WindowedX = (width / 2) + 310
surface4WindowedY = (height / 2) - 360

surface4X = surface4WindowedX
surface4Y = surface4WindowedY

surface5FullscreenX = (monitorX / 2) - 310
surface5FullscreenY = (monitorY / 2) + 60

surface5WindowedX = (width / 2) - 310
surface5WindowedY = (height / 2) + 60

surface5X = surface5WindowedX
surface5Y = surface5WindowedY

surface6FullscreenX = (monitorX / 2) + 10
surface6FullscreenY = (monitorY / 2) + 60

surface6WindowedX = (width / 2) + 10
surface6WindowedY = (height / 2) + 60

surface6X = surface6WindowedX
surface6Y = surface6WindowedY

screen = pygame.display.set_mode(size)

surface1 = pygame.Surface((1300,720))
surface2 = pygame.Surface((1000,600))
surface3 = pygame.Surface((340,340))
surface4 = pygame.Surface((340,340))
surface5 = pygame.Surface((300,300))
surface6 = pygame.Surface((300,300))

surface2.set_colorkey(0x0000FF)
surface3.set_colorkey(0x0000FF)
surface4.set_colorkey(0x0000FF)
surface5.set_colorkey(0x0000FF)
surface6.set_colorkey(0x0000FF)

screen.fill(0x000000)

fifeteen = pygame.font.SysFont("Droid Sans", 15)

twenty = pygame.font.SysFont("Droid Sans", 18)

sixty = pygame.font.SysFont("Droid Sans", 60)

BLACK = (0,0,0)
RED = (30,0,0)
PINK = (255,105,180)
PURPLE = (128,0,128)
WHITE = (255,255,255)
BLUE = (136,196,255)

#degree = u'\N{DEGREE CELSIUS}'
percent = u'\N{PERCENT SIGN}'
millivolt = 'mV'
volt = 'V'

degree = u"\u00B0"

pygame.mouse.set_visible(False)

def indicatorLegend(
                    legendValue,
                    displayValue,
                    positionX,
                    positionY,
                    length,
                    destination,
                    fontSize,
                    doubleLength=False,
                    drawLine=True,
                    doubleLine=6,
                    singleLine=3,
                    displayDivision=1,
                    backgroundColour = RED,
                    dialType = False

    ):

        position = (positionX,positionY)

        if doubleLength:
            lineLength = doubleLine
        else:
            lineLength = singleLine

        x = position[0] - math.cos(math.radians(legendValue)) * length
        y = position[1] - math.sin(math.radians(legendValue)) * length
        xa = position[0] - math.cos(math.radians(legendValue)) * (length - int(length / lineLength))
        ya = position[1] - math.sin(math.radians(legendValue)) * (length - int(length / lineLength))
        xlabel = position[0] - math.cos(math.radians(legendValue)) * (length - int(length / singleLine))
        ylabel = position[1] - math.sin(math.radians(legendValue)) * (length - int(length / singleLine))

        if drawLine:
            pygame.draw.aaline(destination, BLUE, (x,y),(xa,ya), False)

        if dialType:
            label = fontSize.render(("%s%s" % ((displayValue / displayDivision),dialType)),
                                    1, BLUE, backgroundColour)
        else:
            label = fontSize.render((str(displayValue / displayDivision)),
                                    1, BLUE, backgroundColour)

        labelRect = label.get_rect()
        labelRect.centerx = int(xlabel)
        labelRect.centery = int(ylabel)# + 5
        destination.blit(label, (labelRect))


def indicatorNeedle(
                    needleDestination,
                    needleValue = 0,
                    needleLength = 358,
                    positionX = 600,
                    positionY = 360,
                    fontSize = sixty,
                    backgroundColour = BLACK,
                    startPosition = 0,
                    endPosition = 0,
                    maximumValue = 10,
                    doubleLine = 6,
                    singleLine = 3,
                    displayDivision = 1,
                    displayNeedle = True,
                    displayCircle = True,
                    dialLabel = False,
                    dialType = False
    ):

    position = (positionX,positionY)
    length = needleLength
    length2 = int(needleLength / 20)
    length3 = length2 + 5
    destination = needleDestination
    fontSize = fontSize
    singleLine = singleLine
    doubleLine = doubleLine
    backgroundColour = backgroundColour


    degreesDifference = 360 - (startPosition + (180 - endPosition))
    value = int((needleValue * (degreesDifference / (maximumValue * 10.0))) + startPosition)
    displayValue = (needleValue * (degreesDifference / (maximumValue * 10.0))) + startPosition

    x = position[0] - math.cos(math.radians(value)) * (length - int(length / singleLine))
    y = position[1] - math.sin(math.radians(value)) * (length - int(length / singleLine))
    x2 = position[0] - math.cos(math.radians(value - 90)) * length2
    y2 = position[1] - math.sin(math.radians(value - 90)) * length2
    x3 = position[0] - math.cos(math.radians(value + 180)) * length3
    y3 = position[1] - math.sin(math.radians(value + 180)) * length3
    x4 = position[0] - math.cos(math.radians(value + 90)) * length2
    y4 = position[1] - math.sin(math.radians(value + 90)) * length2

    xa = position[0] - math.cos(math.radians(value)) * length
    ya = position[1] - math.sin(math.radians(value)) * length
    xa2 = x - math.cos(math.radians(value))
    ya2 = y - math.sin(math.radians(value))
    xa3 = x - math.cos(math.radians(value + 180))
    ya3 = y - math.sin(math.radians(value + 180))
    xa4 = x - math.cos(math.radians(value + 90)) * (length2 + 4)
    ya4 = y - math.sin(math.radians(value + 90)) * (length2 + 4)

    if displayCircle:
        #pygame.gfxdraw.aacircle(destination,position[0],position[1], length, RED)
        pygame.draw.circle(destination, RED, (position[0],position[1]), length , 0)

    if dialLabel:
        showLabel = fontSize.render(dialLabel, 1, BLUE, backgroundColour)
        labelRect = showLabel.get_rect()
        labelRect.centerx = position[0]
        labelRect.centery = position[1] - 30
        destination.blit(showLabel, (labelRect))

    valueDivisions = degreesDifference / 10

    indicatorLegend(startPosition, 0, position[0], position[1], length,
                    destination, fontSize,False,True,doubleLine,singleLine,1,backgroundColour)

    for divisions in range(1,10):

        if needleValue >= (maximumValue * divisions):
            indicatorLegend((startPosition + (valueDivisions * divisions)), (maximumValue * divisions),
                            position[0], position[1], length, destination, fontSize,True,True,doubleLine
                            ,singleLine,displayDivision,backgroundColour)

    if displayNeedle:
        pygame.draw.aalines(destination, BLUE, True, ((x,y), (x2,y2), (x3, y3), (x4, y4)), False)


    pygame.gfxdraw.arc(destination,position[0],position[1],
                       (length - int(length / singleLine)),(180 + value),endPosition,  BLUE)

    pygame.draw.aaline(destination, BLUE, (x,y),(xa,ya), False)

    pygame.gfxdraw.arc(destination,position[0],position[1],
                       length,(180 + startPosition), (value - 180), BLUE)

    pygame.gfxdraw.arc(destination,position[0],position[1],
                       (length - int(length / doubleLine)),(180 + startPosition) , (value - 180), BLUE)

    if dialType:
        indicatorLegend((180 + endPosition), needleValue, position[0], position[1],
                        length, destination, fontSize, False, False,
                        doubleLine,singleLine,1,backgroundColour,dialType)
    else:
        indicatorLegend((180 + endPosition), needleValue , position[0], position[1],
                        length, destination, fontSize, False, False,
                        doubleLine,singleLine,1,backgroundColour)


READ_THREAD = False
MPH_Value = 0
RPM_Value = 0
TEMP_Value = 0
BATT_Value = 0
AAC_Value = 0
MAF_Value = 0

while READ_THREAD == False:

    try:

        PORT.flushInput()
        PORT.write('\xFF\xFF\xEF')
        time.sleep(2)
        Connected = PORT.read(1)
        if Connected == '\x10':

            READ_THREAD = True
            ReadStream(True)

    except ValueError:

            PORT.open()


while READ_THREAD == True:

    pygame.time.Clock().tick(60)

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            PORT.flushInput()
            PORT.close()
            sys.exit()

        if event.type is KEYDOWN and event.key == K_q:
            PORT.flushInput()
            PORT.close()
            sys.exit()

        if event.type is KEYDOWN and event.key == K_w:
            pygame.display.set_mode((width,height))
            pygame.mouse.set_visible(False)
            surface1X = surface1WindowedX
            surface1Y = surface1WindowedY
            surface2X = surface2WindowedX
            surface2Y = surface2WindowedY
            surface3X = surface3WindowedX
            surface3Y = surface3WindowedY
            surface4X = surface4WindowedX
            surface4Y = surface4WindowedY
            surface5X = surface5WindowedX
            surface5Y = surface5WindowedY
            surface6X = surface6WindowedX
            surface6Y = surface6WindowedY
            screen.fill(0x000000)

        if event.type is KEYDOWN and event.key == K_f:
            pygame.display.set_mode((monitorX,monitorY), FULLSCREEN)
            surface1X = surface1FullscreenX
            surface1Y = surface1FullscreenY
            surface2X = surface2FullscreenX
            surface2Y = surface2FullscreenY
            surface3X = surface3FullscreenX
            surface3Y = surface3FullscreenY
            surface4X = surface4FullscreenX
            surface4Y = surface4FullscreenY
            surface5X = surface5FullscreenX
            surface5Y = surface5FullscreenY
            surface6X = surface6FullscreenX
            surface6Y = surface6FullscreenY
            screen.fill(0x000000)
            pygame.mouse.set_visible(False)

    surface1.fill(0x000000)
    surface2.fill(0x0000FF)
    surface3.fill(0x0000FF)
    surface4.fill(0x0000FF)
    surface5.fill(0x0000FF)
    surface6.fill(0x0000FF)

    indicatorNeedle(surface1,MPH_Value,648,650,650,sixty,BLACK,0,0,10,12,6,1,False,False)
    indicatorNeedle(surface2,RPM_Value,488,500,500,sixty,BLACK,0,0,500,10,5,100,False,False)
    indicatorNeedle(surface3,MAF_Value,168,170,170,twenty,BLACK,-45,-45,50,6,3,10,True,False,"MAF",millivolt)
    indicatorNeedle(surface4,AAC_Value,168,170,170,twenty,BLACK,45,45,10,6,3,1,True,False,"AAC",percent)
    indicatorNeedle(surface5,TEMP_Value,148,150,150,twenty,BLACK,-45,45,16,6,3,1,True,False,"Temperature",degree)
    indicatorNeedle(surface6,BATT_Value,148,150,150,twenty,BLACK,-45,45,2,6,3,1,True,False,"Battery",volt)


    screen.blit(surface1,(surface1X,surface1Y))
    screen.blit(surface2,(surface2X,surface2Y))
    screen.blit(surface3,(surface3X,surface3Y))
    screen.blit(surface4,(surface4X,surface4Y))
    screen.blit(surface5,(surface5X,surface5Y))
    screen.blit(surface6,(surface6X,surface6Y))

    #time.sleep(0.02)

    pygame.display.update()
