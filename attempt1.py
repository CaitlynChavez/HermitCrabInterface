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

from io import StringIO  #io
import pandas as pd
#https://streamlit.io/
#streamlit run example.py [ARGUMENTS]
print("STARTING!")
st.write("# hermit crabs *yee haw*")
secondInterval = 0
# while secondInterval >= 5 and secondInterval <= 60:
# secondInterval = st.number_input('Insert an interval between 5 and 60')
secondInterval = st.number_input("Insert a time tracking interval in seconds", min_value=5, max_value=60, step=1)
st.write('Tracking Interval', secondInterval, "seconds")

import tempfile
video_file = st.file_uploader("Please enter the video to label ", accept_multiple_files=False, type = ["mp4", "mov", "avi", "asf", "m4v"])
tfflie = tempfile.NamedTemporaryFile(suffix=".mp4", delete = False)
# if video_file is not None:
#      print("you did it :D")
#
if not video_file:
     # To read file as bytes:
     # To read file as bytes:
     # bytes_data = video_file.getvalue()
     # # st.write(bytes_data)
     #
     # # To convert to a string based IO:
     # stringio = StringIO(video_file.getvalue().decode("utf-8"))
     # # st.write(stringio)
     #
     # # To read file as string:
     # string_data = stringio.read()
     # # st.write(string_data)
     # print(string_data)

     # Can be used wherever a "file-like" object is accepted:
     # dataframe = pd.read_csv(video_file, encoding='latin-1')
     # print(type(dataframe))
     # st.write(dataframe)
     # vs = cv2.VideoCapture(dataframe)

# https://www.youtube.com/watch?v=mxRH275SyAU

     tfflie.write(video_file)
     vid = open(tfflie.name, 'rb')
     vid_bytes = vid.read()

     st.sidebar.text("input video")
     st.sidebar.video(vid_bytes)

# while video_file is not None:
#     print(type(video_file))
#     print("you did it!")
#     break
# # test = st.slider('hi?', 0, 130, 25)
# #



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

#
# if not vs.isOpened():
#     print("Video cannot be opened")
#     sys.exit()
# # resize_dim = 800
# ret, first_frame = vs.read()
# max_dim = max(first_frame.shape)
# scale = resize_dim/max_dim
# print(max_dim)
# # Read first frame.
# ok, frame = vs.read()
