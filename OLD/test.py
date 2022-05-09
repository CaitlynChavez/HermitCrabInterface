import CrabTracker
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import math
import streamlit as st
import os #folder creation
from os import listdir
from os.path import isfile, join
import csv
#writes to excel
import xlsxwriter

vid = cv2.VideoCapture("Bob_and_aws.mov")
secondInterval = 30
crabTrack = CrabTracker.CrabTracker(2, True, True, vid, "TESTOUTPUTNAME", int(secondInterval))
crabTrack.startAnalyzingVideo()
