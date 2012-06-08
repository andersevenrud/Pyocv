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
import ocv
from config import *

# ########################################################################### #
# APPLICATION                                                                 #
# ########################################################################### #

# Class: Tracker
class Tracker(ocv.CVApplication):

    def __init__(self, path, capture_id = 0):
        self.path_img     = "%s/_output.jpg" % path
        self.path_txt     = "%s/_output" % path

        self.capture      = ocv.CVCapture(capture_id)

        self.win_result   = ResultsWindow()
        self.win_settings = SettingsWindow()

        ocv.CVApplication.__init__(self)

    def handle(self, frame, settings):
        """Handle Frame Manipulation"""
        img = ocv.CVCopyGrayscale(frame)
        try:
            cv.Threshold(img, img, settings["Threshold"], 255, settings["Type"]);
        except:
            pass

        if settings["Equalize"]:
            cv.EqualizeHist(img, img)

        ocv.CVBrightnessContrast(img, settings["Contrast"], settings["Brightness"]);

        return img

    def run(self):
        """Main Loop"""
        capture_toggled = False
        while 1:
            # Capture Frame(s)
            opts  = self.win_settings.settings
            frame = self.capture.poll(opts["Flip"])
            result = None
            if frame is None:
                break

            img = self.handle(frame, opts)

            # Keyboard Handling
            k = cv.WaitKey(10)
            if k == 113: # q
                print "Exiting..."
                break
            elif k == 99: # c
                print ">>> Detecting Text..."
                result = self.detect_text(img)
                print "<<< DONE"
            elif k == 102: # f
                print ">>> Detecting Object(s)..."
                result = self.detect_objects(img, opts["Haarcascade"])
                print "<<< DONE"
            elif k == 116: # t
                capture_toggled = not capture_toggled

            # Render Output
            if capture_toggled:
                self.win_settings.render(frame)
            else:
                self.win_settings.render(img)

            if result is not None:
                self.win_result.render(result)



        self.stop()

    def detect_text(self, frame):
        """Detect text in given frame, return image with result"""
        img = cv.CreateImage((320, 240), cv.IPL_DEPTH_8U, frame.nChannels)

        psm = self.win_settings.settings["Pagesegmode"]
        data = ocv.CVReadText(frame, self.path_img, self.path_txt, psm)
        if data is None:
            data = "Empty..."

        result = ocv.CVText(img, data, 10, 15, 15, self.font, True)

        cv.Copy(result, img)

        return img

    def detect_objects(self, frame, haar):
        """Detect objects in given frame, return image with result"""
        img = cv.CreateImage((320, 240), cv.IPL_DEPTH_8U, frame.nChannels)
        objects = ocv.CVObjects(frame, self.storage, HAARS[haar])

        ocv.CVClear(img)
        if objects:
            cv.Resize(objects, img)

        return img

# ########################################################################### #
# WINDOWS                                                                     #
# ########################################################################### #

# Class: ResultsWindow
class ResultsWindow(ocv.CVWindow):
    def __init__(self):
        ocv.CVWindow.__init__(self, "Results", 0, 0, 800, 600)

    def render(self, frame = None):
        # We want a smaller preview
        img = cv.CreateImage((800, 600), cv.IPL_DEPTH_8U, frame.nChannels)
        if frame is not None:
            cv.Resize(frame, img)

        ocv.CVWindow.render(self, img)

# Class: SettingsWindow
class SettingsWindow(ocv.CVWindow):
    def __init__(self):
        ocv.CVWindow.__init__(self, "Settings", 950, 0)

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
        img = cv.CreateImage((320, 240), cv.IPL_DEPTH_8U, frame.nChannels)
        cv.Resize(frame, img)
        ocv.CVWindow.render(self, img)

# ########################################################################### #
# MAIN                                                                        #
# ########################################################################### #

if __name__ == "__main__":
    app = Tracker(DEFAULT_TMP, DEFAULT_DEV)
    print """PyOCV Example

Press q - To quit
      c - Capture Text
      f - Capture Object
      t - Toggle Capture/Image in view

"""

    app.run()

