import streamlit as st
# import pandas as pd


from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import math

import os #folder creation
from os import listdir
from os.path import isfile, join
import csv
#writes to excel
import xlsxwriter
#https://streamlit.io/
#streamlit run example.py [ARGUMENTS]
st.write("# hermit crabs *yee haw*")
secondInterval = 0
# while secondInterval >= 5 and secondInterval <= 60:
# secondInterval = st.number_input('Insert an interval between 5 and 60')
secondInterval = st.number_input("Insert a number between 5 and 60 for seconds", min_value=5, max_value=60, step=1)
st.write('The current number is ', secondInterval)


video_file = st.file_uploader("Please enter the video to label ")
# if video_file is not None:
#     print("you did it :D")
# # test = st.slider('hi?', 0, 130, 25)
# #
# vs = cv2.VideoCapture(video_file)


# OpenCV object tracker implementations  #KCF, fast acc, csrt, most accurate but slower, mosse fast but inaccurate
# OPENCV_OBJECT_TRACKERS = {
#     "csrt": cv2.TrackerCSRT_create,
#     "kcf": cv2.TrackerKCF_create,
#     "boosting": cv2.TrackerBoosting_create,
#     "mil": cv2.TrackerMIL_create,
#     "tld": cv2.TrackerTLD_create,
#     "medianflow": cv2.TrackerMedianFlow_create,
#     "mosse": cv2.TrackerMOSSE_create
# }
# trackers = cv2.MultiTracker_create()
# # tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']
# # tracker_type = tracker_types[5]
# tracker_type = "csrt"
#
# number_of_crabs_to_track = int(input("Please enter number of crabs to track:\n"))


if not vs.isOpened():
    print("Video cannot be opened")
#     sys.exit()
# # resize_dim = 800
# ret, first_frame = vs.read()
# max_dim = max(first_frame.shape)
# scale = resize_dim/max_dim
# print(max_dim)
# # Read first frame.
# ok, frame = vs.read()
