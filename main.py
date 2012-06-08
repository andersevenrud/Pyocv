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

        self.win_capture  = CaptureWindow()
        self.win_output   = OutputWindow()
        self.win_result   = ResultsWindow()
        self.win_settings = SettingsWindow()

        ocv.CVApplication.__init__(self)

    def handle(self, frame, settings):
        """Handle Frame Manipulation"""
        img = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(frame, img, cv.CV_RGB2GRAY)
        try:
            cv.Threshold(img, img, settings["Threshold"], 255, settings["Type"]);
        except:
            pass

        if settings["Equalize"]:
            cv.EqualizeHist(img, img)

        return img

    def run(self):
        """Main Loop"""
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
                print ">>> Detecting Face..."
                result = self.detect_face(img)
                print "<<< DONE"

            # Render Output
            self.win_capture.render(frame)
            self.win_output.render(img)
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

    def detect_face(self, frame):
        """Detect face in given frame, return image with result"""
        img = cv.CreateImage((320, 240), cv.IPL_DEPTH_8U, frame.nChannels)
        face = ocv.CVFaces(frame, self.storage)

        ocv.CVClear(img)
        if face:
            cv.Resize(face, img)

        return img

# ########################################################################### #
# WINDOWS                                                                     #
# ########################################################################### #

# Class: CaptureWindow
class CaptureWindow(ocv.CVWindow):
    def __init__(self):
        ocv.CVWindow.__init__(self, "Capture Device", 0, 0)

    def render(self, frame):
        # We want a smaller preview
        img = cv.CreateImage((320, 240), cv.IPL_DEPTH_8U, frame.nChannels)
        cv.Resize(frame, img)
        ocv.CVWindow.render(self, img)

# Class: OutputWindow
class OutputWindow(ocv.CVWindow):
    def __init__(self):
        ocv.CVWindow.__init__(self, "Output", 330, 0)

# Class: ResultsWindow
class ResultsWindow(ocv.CVWindow):
    def __init__(self):
        ocv.CVWindow.__init__(self, "Results", 0, 265)

# Class: SettingsWindow
class SettingsWindow(ocv.CVWindow):
    def __init__(self):
        ocv.CVWindow.__init__(self, "Settings", 0, 530)

        self.createTrackbar("Flip", DEFAULT_FLIP, 1)
        self.createTrackbar("Type", DEFAULT_TYPE, 4)
        self.createTrackbar("Threshold", DEFAULT_THRESHOLD, 255)
        self.createTrackbar("Equalize", DEFAULT_EQUALIZE, 1)
        self.createTrackbar("Pagesegmode", DEFAULT_PSM, 10)

# ########################################################################### #
# MAIN                                                                        #
# ########################################################################### #
if __name__ == "__main__":
    app = Tracker(DEFAULT_TMP, DEFAULT_DEV)
    print "Press 'q' to quit, 'c' to capture text, 'f' to detect face..."
    app.run()
