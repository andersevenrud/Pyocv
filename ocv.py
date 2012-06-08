#!/usr/bin/env python
#
# PyOCV - Python OpenCV
# ocv.py - Main Pyocv Library
#
# Author: Anders Evenrud <andersevenrud@gmail.com>
# License: Simple BSD
#

import cv
import os

from config import *

# ########################################################################### #
# FUNCTIONS                                                                   #
# ########################################################################### #

def CVCopyGrayscale(frame):
    """Copy frame and convert to GrayScale"""
    img = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, 1)
    cv.CvtColor(frame, img, cv.CV_RGB2GRAY)
    return img

def CVClear(frame):
    """Clear a Frame"""
    cv.Set(frame, (0, 0, 0));

def CVObjects(frame, storage, haar):
    """Read Objects from Frame"""
    cascade = cv.Load("%s/%s.%s" % (HAAR_PATH, haar, "xml"))
    objects = cv.HaarDetectObjects(frame, cascade, storage, 1.2, 2, 0, (20, 20))
    if objects:
        for ((x, y, w, h), n) in objects:
            return cv.GetSubRect(frame, (x, y, w, h))

    return None

def CVText(frame, text, x = 0, y = 0, step = 15, font = None, clear = False):
    """Apply text to an image"""
    img = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, frame.nChannels)

    if font is None:
        font = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 0.9, 0.9, 0, 1, 1)

    if clear:
        CVClear(img)

    for i in text.split("\n"):
        i = i.strip()
        if i:
            cv.PutText(img, i, (x, y), font, 255)
            y += step;

    return img

def CVReadText(frame, name, out, psm = 3, lang = DEFAULT_LANGUAGE):
    """Read Text From Image"""
    data = None

    # Save image
    cv.SaveImage(name, frame);
    if os.path.isfile(name):
        # Detect text
        #cmd = "tesseract -psm %d -lang %s %s %s" % (psm, lang, name, out)
        cmd = "tesseract -psm %d %s %s" % (psm, name, out)
        print "Executing '%s'" % cmd
        os.system(cmd)
        out += ".txt"
        if os.path.isfile(out):
            # Store result
            data = open(out, 'r').read()
            if not data.strip():
                data = None
    return data

# ########################################################################### #
# CLASSES                                                                     #
# ########################################################################### #

#
# Class: CVApplication -- OpenCV Default Application
#
class CVApplication:

    def __init__(self, id=0):
        """Create a new OpenCV Application"""
        self.storage      = cv.CreateMemStorage(id)
        self.font         = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 0.9, 0.9, 0, 1, 1)

    def run(self):
        """Start Application"""
        pass

    def stop(self):
        """Stop Application"""
        try:
            cv.ClearMemStorage(self.storage)
        except:
            pass

#
# Class: CVCapture -- OpenCV Capture Device Instance
#
class CVCapture:

    def __init__(self, id=0, width=640, height=480):
        """Create a new OpenCV Capture Device"""
        self.capture = cv.CreateCameraCapture(id)
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_WIDTH, width)
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, height)


    def poll(self, flip = False):
        """Get a frame from device"""
        frame = cv.QueryFrame(self.capture)
        #img = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, frame.nChannels)
        #cv.Copy(frame, img)
        if flip:
            cv.Flip(frame, None, 1)
        return frame

#
# Class: CVWindow -- OpenCV Window Abstraction
#
class CVWindow:

    def __init__(self, name, x = -1, y = -1, w = None, h = None):
      """Create OpenCV Window"""

      if w is not None and h is not None:
          cv.NamedWindow(name, 0)
          cv.ResizeWindow(name, w, h)
      else:
          cv.NamedWindow(name, cv.CV_WINDOW_AUTOSIZE)

      if x != -1 and y != -1:
          cv.MoveWindow(name, x, y)

      self.name     = name
      self.settings = {}

    def __del__(self):
        """Remove OpenCV Window"""
        try:
            cv.DestroyWindow(self.name)
        except:
            pass

    def createTrackbar(self, name, val = 0, maxval = 255):
        """Insert a new Trackbar"""
        def wrapper(a):
            self.handleTrackbarEvent(name, a)

        cv.CreateTrackbar(name, self.name, val, maxval, wrapper)
        wrapper(val)

    def handleTrackbarEvent(self, name, val):
        """Handle Trackbar onchange"""
        self.settings[name] = int(val)

    def render(self, frame):
        """Render the selected frame"""
        cv.ShowImage(self.name, frame)

