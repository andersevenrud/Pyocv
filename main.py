#!/usr/bin/env python
#
# PyOCV - Python OpenCV
# main.py - Example File
#
# Author: Anders Evenrud <andersevenrud@gmail.com>
# License: Simple BSD
#

# Dependencies
import cv
import pprint

# Locals
from ocv import *
from config import *

# ########################################################################### #
# APPLICATION                                                                 #
# ########################################################################### #

# Class: Tracker
class Tracker(OCVApplication):

    def __init__(self, path, capture_id = 0):
        self.path_img     = "%s/_output.jpg" % path
        self.path_txt     = "%s/_output" % path

        self.capture      = OCVCapture(capture_id)

        self.win_result   = ResultsWindow()
        self.win_settings = SettingsWindow()

        OCVApplication.__init__(self)

    def handle(self, frame, settings, bw):
        """Handle Frame Manipulation"""
        if bw:
            img = OCVCopyGrayscale(frame)
        else:
            img = OCVCloneImage(frame)

        if bw:
            try:
                cv.Threshold(img, img, settings["Threshold"], 255, settings["Type"]);
            except:
                pass

            if settings["Equalize"]:
                cv.EqualizeHist(img, img)

        OCVBrightnessContrast(img, settings["Contrast"], settings["Brightness"]);

        return img

    def run(self):
        """Main Loop"""
        capture_mode = 0
        capture_modify = True
        capture_bw = True

        while 1:
            # Capture Frame(s)
            opts  = self.win_settings.settings
            frame = self.capture.poll(opts["Flip"])
            detect = 0

            result = None
            if frame is None:
                break

            # Keyboard Handling
            k = cv.WaitKey(10)
            if k == 113: # q
                print "Exiting..."
                break
            elif k == 99: # c
                print ">>> Detecting Text..."
                detect = 1
            elif k == 102: # f
                print ">>> Detecting Object(s)..."
                detect = 2
            elif k == 116: # t
                capture_mode += 1
                if capture_mode > 1:
                    capture_mode = 0

                mode = ((["Modified", "Original"])[capture_mode])
                print ">>> Mode: %d - %s" % (capture_mode, mode)
            elif k == 109: # m
                capture_modify = not capture_modify
                if capture_modify:
                    print ">>> Showing: Modified"
                else:
                    print ">>> Showing: Original"
            elif k == 100: # d
                capture_bw = not capture_bw
                if capture_bw:
                    print ">>> B&W: True"
                else:
                    print ">>> B&W: False"

            if capture_modify:
                img = self.handle(frame, opts, capture_bw)
            else:
                img = OCVCloneImage(frame)

            if detect == 1:
                result = self.detect_text(img)
            elif detect == 2:
                result = self.detect_objects(img, opts["Haarcascade"])

            if capture_mode == 0:
                self.win_settings.render(img)
            elif capture_mode == 1:
                hist = OCVHistogram(img)
                self.win_settings.render(hist)

            if result is not None:
                self.win_result.render(result)

        self.stop()

    def detect_text(self, frame):
        """Detect text in given frame, return image with result"""
        img = cv.CreateImage((320, 240), cv.IPL_DEPTH_8U, frame.nChannels)

        psm = self.win_settings.settings["Pagesegmode"]
        data = OCVReadText(frame, self.path_img, self.path_txt, psm)
        pprint.pprint(data)
        if data is None:
            data = "Empty..."

        result = OCVText(img, data, 10, 15, 15, self.font, True)

        cv.Copy(result, img)

        return img

    def detect_objects(self, frame, haar):
        """Detect objects in given frame, return image with result"""
        img = OCVCloneImage(frame)
        objects = OCVObjects(frame, self.storage, HAARS[haar])

        if objects:
            for ((x, y, w, h), n) in objects:
                tl = (x + int(w*0.1), y + int(h*0.07))
                br = (x + int(w*0.9), y + int(h*0.87))
                cv.Rectangle(img, tl, br, (0, 255, 0), 3)

            return img

        return None

# ########################################################################### #
# WINDOWS                                                                     #
# ########################################################################### #

# Class: ResultsWindow
class ResultsWindow(OCVWindow):
    def __init__(self):
        OCVWindow.__init__(self, "Results", 0, 0, 800, 600)

    def render(self, frame = None):
        # We want a bigger preview
        if frame is not None:
            img = OCVResizeImage(frame, (800, 600))
            OCVWindow.render(self, img)

# Class: SettingsWindow
class SettingsWindow(OCVWindow):
    def __init__(self):
        OCVWindow.__init__(self, "Settings", 950, 0)

        self.createTrackbar("Flip",         DEFAULT_FLIP,       1)
        self.createTrackbar("Type",         DEFAULT_TYPE,       4)
        self.createTrackbar("Threshold",    DEFAULT_THRESHOLD,  255)
        self.createTrackbar("Equalize",     DEFAULT_EQUALIZE,   1)
        self.createTrackbar("Pagesegmode",  DEFAULT_PSM,        10)
        self.createTrackbar("Haarcascade",  DEFAULT_HAAR,       9)
        self.createTrackbar("Brightness",   DEFAULT_BRIGHTNESS, 200)
        self.createTrackbar("Contrast",     DEFAULT_CONTRAST,   200)

    def render(self, frame):
        # We want a smaller preview
        img = OCVResizeImage(frame, (320, 240))
        OCVWindow.render(self, img)

# ########################################################################### #
# MAIN                                                                        #
# ########################################################################### #

if __name__ == "__main__":
    app = Tracker(DEFAULT_TMP, DEFAULT_DEV)
    print """PyOCV Example

Press q - To quit
      c - Capture Text
      f - Capture Object
      t - Toggle Preview Mode (Capture/Histogram)
      m - Toggle Image Modification (On/Off)
      d - Toggle B&W (Type/Threshold/Equalize)

"""

    app.run()

