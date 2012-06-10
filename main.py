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
import argparse

# Locals
from ocv import *
from config import *

# ########################################################################### #
# APPLICATION                                                                 #
# ########################################################################### #

# Class: TrackerImage
class TrackerImage(OCVImage):

    def __init__(self, frame, cap_settings, im_settings):
        """Create and modify image"""
        OCVImage.__init__(self, frame)

        if cap_settings["CaptureModify"]:
            if cap_settings["CaptureBW"]:
                self.mode(1)

                try:
                    self.setThreshold(im_settings["Threshold"], im_settings["Type"])
                except:
                    pass

                if im_settings["Equalize"]:
                    self.equalize()


            self.setBrightnessContrast(im_settings["Brightness"], im_settings["Contrast"])

    def detect_text(self, font, psm, path_img, path_txt):
        """Detect text"""
        img   = OCVCloneImage(self.frame)
        data  = OCVReadText(self.frame, path_img, path_txt, psm)
        pprint.pprint(data)
        if data is None:
            data = "Empty..."

        result = OCVText(img, data, 10, 15, 15, font, True)

        cv.Copy(result, img)

        return img

    def detect_objects(self, storage, haar):
        """Detect objects"""
        img     = OCVCloneImage(self.frame)
        objects = OCVObjects(self.frame, storage, HAARS[haar])

        if objects:
            for ((x, y, w, h), n) in objects:
                tl = (x + int(w*0.1), y + int(h*0.07))
                br = (x + int(w*0.9), y + int(h*0.87))
                cv.Rectangle(img, tl, br, (0, 255, 0), 3)

            return img

        return None

# Class: Tracker
class Tracker(OCVApplication):

    def __init__(self, path, capture_id, capture_width, capture_height):
        """Create new Application"""
        self.path_img     = "%s/_output.jpg" % path
        self.path_txt     = "%s/_output" % path
        self.win_result   = ResultsWindow()
        self.win_settings = SettingsWindow()

        # Other settings are handled by GUI, these are key bindings
        self.settings = {
            "PreviewMode"    : 0,
            "CaptureModify"  : True,
            "CaptureBW"      : True
        }

        OCVApplication.__init__(self, 0, capture_id, capture_width, capture_height)

    def handleKey(self, k):
        """Handle Keyboard Input"""
        if k == 113: # q
            print "Exiting..."
            return False
        elif k == 99: # c
            print ">>> Detecting Text..."
            return "text"
        elif k == 102: # f
            print ">>> Detecting Object(s)..."
            return "object"
        elif k == 116: # t
            self.settings["PreviewMode"] += 1
            if self.settings["PreviewMode"] > 1:
                self.settings["PreviewMode"] = 0

            mode = ((["Capture", "Histogram"])[self.settings["PreviewMode"]])
            print ">>> Mode: %d - %s" % (self.settings["PreviewMode"], mode)
        elif k == 109: # m
            self.settings["CaptureModify"] = not self.settings["CaptureModify"]
            if self.settings["CaptureModify"]:
                print ">>> Showing: Modified"
            else:
                print ">>> Showing: Original"
        elif k == 98: # b
            self.settings["CaptureBW"] = not self.settings["CaptureBW"]
            if self.settings["CaptureBW"]:
                print ">>> B&W: True"
            else:
                print ">>> B&W: False"

        return True

    def run(self):
        """Main Loop"""

        result = None
        while 1:
            # Get frame and key
            frame, k = OCVApplication.run(self, self.win_settings.settings["Flip"])
            if frame is None:
                break

            # Keyboard Handling
            detect = self.handleKey(k)
            if detect == False:
                break

            # Frame Handling
            img = TrackerImage(frame, self.settings, self.win_settings.settings)

            if detect == "text":
                result = img.detect_text(self.font, self.win_settings.settings["Pagesegmode"], self.path_img, self.path_txt)
            elif detect == "object":
                result = img.detect_objects(self.storage, self.win_settings.settings["Haarcascade"])

            # Output Handling
            if self.settings["PreviewMode"] == 0:
                self.win_settings.render(img.frame)
            elif self.settings["PreviewMode"] == 1:
                self.win_settings.render(img.getHistogram())

            if result is not None:
                self.win_result.render(result)

        # Main loop break
        self.stop()

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
    cap_id      = DEFAULT_DEV
    cap_width   = DEFAULT_DEV_WIDTH
    cap_height  = DEFAULT_DEV_HEIGHT

    parser = argparse.ArgumentParser(description='PyOCV Example Help')
    parser.add_argument('--device', action='store', type=int,
                       help='the capture device id (default: %d)' % cap_id)
    parser.add_argument('--width', action='store', type=int,
                       help='the capture width in pixels (default: %d)' % cap_width)
    parser.add_argument('--height', action='store', type=int,
                       help='the capture height in pixels (default: %d)' % cap_height)

    args = parser.parse_args()
    try:
        cap_id = int(args.device)
    except:
        pass

    try:
        cap_width = int(args.width)
    except:
        pass

    try:
        cap_height = int(args.height)
    except:
        pass

    app = Tracker(DEFAULT_TMP, cap_id, cap_width, cap_height)
    print """PyOCV Example

Press q - To quit
      c - Capture Text
      f - Capture Object
      t - Toggle Preview Mode (Capture/Histogram)
      m - Toggle Image Modification (On/Off)
      b - Toggle B&W (Type/Threshold/Equalize)

"""

    app.run()

