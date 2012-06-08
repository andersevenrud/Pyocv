#!/usr/bin/env python
#
# PyOCV - Python OpenCV
# config.py - Main Pyocv Configuration
#
# Author: Anders Evenrud <andersevenrud@gmail.com>
# License: Simple BSD
#
import os

# Default Settings
DEFAULT_LANGUAGE    = "nor"
DEFAULT_TMP         = os.getcwd()
DEFAULT_DEV         = 1
DEFAULT_DEV_WIDTH   = 640
DEFAULT_DEV_HEIGHT  = 480
DEFAULT_FLIP        = 0
DEFAULT_TYPE        = 3
DEFAULT_THRESHOLD   = 128
DEFAULT_EQUALIZE    = 0
DEFAULT_PSM         = 3
DEFAULT_HAAR        = 4
DEFAULT_BRIGHTNESS  = 0
DEFAULT_CONTRAST    = 0
HAAR_PATH           = "/usr/share/opencv/haarcascades"
TESSERACT_BIN       = "tesseract"

HAARS = [
  "haarcascade_lowerbody",
  "haarcascade_mcs_mouth",
  "haarcascade_lefteye_2splits",
  "haarcascade_frontalface_default",
  "haarcascade_frontalface_alt_tree",
  "haarcascade_upperbody",
  "haarcascade_mcs_nose",
  "haarcascade_mcs_eyepair_small",
  "haarcascade_mcs_leftear",
  "haarcascade_righteye_2splits",
  "haarcascade_fullbody",
  "haarcascade_mcs_righteye",
  "haarcascade_eye",
  "haarcascade_mcs_lefteye",
  "haarcascade_mcs_rightear",
  "haarcascade_mcs_eyepair_big",
  "haarcascade_mcs_upperbody",
  "haarcascade_frontalface_alt2",
  "haarcascade_profileface",
  "haarcascade_eye_tree_eyeglasses",
  "haarcascade_frontalface_alt"
]

