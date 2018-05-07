#!/usr/bin/env python

#from pymouse import PyMouse
import win32api, win32con
from time import sleep
import factory
import calib
import serial
import cPickle
#import svm_lda

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

# Create a Calibrator object.
a = calib.Calibrator()

# Open up the serial port.
ser = serial.Serial('COM9', 9600)

# Deserialize the stored dataset from calibration
# Extract the lists of tuples of values from the dict.
ref = cPickle.load(open('datasets.p', 'rb'))
ref = ref.values()

#svm_lda.__init__('')

#mouse = PyMouse()

# Screen resolution length and height.
#resL, resH = mouse.screen_size()[0], mouse.screen_size()[1]
#lengthCenter, heightCenter = resL/2, resH/2

# Pixels to move by. Vertical is 1 and corresponding
# horizontal for diagonal movement is calculated.
#verticalMove = 1
#horizontalMove = (resL/float(resH)) * verticalMove

# Place the cursor at the center of the screen initially.
#mouse.move(lengthCenter, heightCenter)

# Watch for eye movements, classify and move cursor.
while True:
    readingList = []
    count = 0

    # maxVal is the size of the dataset as specified by the user.
    #print a.maxVal
    while (count < int(a.maxVal)):
        try:
            #print 'GOT HERE'
            arr = ser.readline().strip('\x00\r\n').strip().split(',')
            #print arr[0] + ',' + arr[1]
            readingList.append((float(arr[0]), float(arr[1])))
        except:
            continue
        count = count + 1
        #print count
    # Calculate similarity, scale and classify.
    scaled = factory.scale([factory.retSimilarity(readingList, ref, 1), \
                            factory.retSimilarity(readingList, ref, 2), \
                            factory.retSimilarity(readingList, ref, 3), \
                            factory.retSimilarity(readingList, ref, 4)])
    direction = factory.classify(scaled)
    
    #direction = svm_lda.svm_predict(readingList)
    print direction

    #l, h = mouse.position()[0], mouse.position()[1]
    #mouse.move(l, h)

    # Decrease or increase the vertical/horizontal position based on the
    # direction of the eyes.
    if direction == "STRAIGHT":
        #print direction
        pass
    elif direction == "UP":
        win32api.SetCursorPos((1366/2,0))
##    elif direction == "UP-RIGHT":
##        win32api.SetCursorPos((1366,0))
    elif direction == "RIGHT":
        win32api.SetCursorPos((1366,768/2))
##    elif direction == "DOWN-RIGHT":
##        win32api.SetCursorPos((1366,768))
    elif direction == "DOWN":
        win32api.SetCursorPos((1366/2,768))
##    elif direction == "DOWN-LEFT":
##        win32api.SetCursorPos((0,768))
    elif direction == "LEFT":
        win32api.SetCursorPos((0,768/2))
##    elif direction == "UP-LEFT":
##        win32api.SetCursorPos((0,0))
    elif direction == "BLINK":
        click(1366/2,768/2)

    # Clear input buffer before iterating.
    ser.flushInput()
