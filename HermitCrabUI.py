import streamlit as st
# import pandas as pd
# streamlit run attempt2.py

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
import numpy as np
import tempfile

import CrabTracker
#https://streamlit.io/
#streamlit run attempt2.py [ARGUMENTS]



def main():
    print("STARTING")
    st.title("Object Tracking Dashboard")

    # create a settings bar to the left of the screen
    st.sidebar.title("settings")
    st.markdown(
    """
    <style>
    [data-testid = "stSidebar"][area-expanded = "true"] > div:first-child{width: 400px;}
    [data-testid = "stSidebar"][area-expanded = "false"] > div:first-child{width: 400px; margin-left: -400px}
    </style>
    """,
    )
    unsafe_allow_html = True
    stframe = st.empty()
    st.sidebar.markdown("---")

    # columns for labeling videos
    kpi1, kpi2, = st.columns(2)

    # initialize column values
    # with kpi1:
    #     st.markdown("**Seconds Interval**")
    #     kpi1_text = st.markdown("0")
    # with kpi2:
    #     st.markdown("**Number of Crabs**")
    #     kpi2_text = st.markdown("0")

    # TO-DO: FILL IN ADDITIONAL CODE FOR OPENCV TRACKING



    # allow user to save the labeled video (checkbox)
    save_img = st.sidebar.checkbox("Save Video")

    # allow user to upload a video
    video_file_buffer = st.sidebar.file_uploader("Upload a Video", type = ["mp4", "mov", "avi", "asf", "m4v"])
    # display a demo video at first
    demo_video = "Bob_and_aws.mov"
    tfflie = tempfile.NamedTemporaryFile(delete = False)
    video_uploaded_bool = False

    # No video uploaded
    if not video_file_buffer:
        pass
        # vid = cv2.VideoCapture(demo_video)
        # tfflie.name = demo_video
    else : # Video properly uploaded
        video_uploaded_bool = True
        # get input of tracking interval in seconds
        secondInterval = st.number_input("Insert a time tracking interval in seconds", min_value=0, max_value=60, step=1)
        # get input of number of crabs to track
        numCrabs = st.number_input("Insert the number of crabs to track", min_value=0, max_value=60, step=1)
        # display input values
        with kpi1:
            st.markdown("**Seconds Interval**")
            kpi1_text = st.markdown(secondInterval)
        with kpi2:
            st.markdown("**Number of Crabs**")
            kpi2_text = st.markdown(numCrabs)
        # adds a start button and only plays the video if pressed and the inputs are not 0
        inputsReady = (secondInterval != 0) and (numCrabs != 0)
        if st.button("Start Video") and inputsReady:

            if inputsReady:
                tfflie.write(video_file_buffer.read())
                vid = cv2.VideoCapture(tfflie.name)
                print(tfflie.name)
                crabTrack = CrabTracker.CrabTracker(numCrabs, False, False, vid, "genericname")
                crabTrack.startAnalyzingVideo()

        #number_of_crabs_to_track, write_to_excel, write_to_video, video, video_name):
        # crabTrack = CrabTracker.CrabTracker(numCrabs, False, False, vid, "genericname")
        # crabTrack.startAnalyzingVideo()
        # while(vid.isOpened()):
        #     # capture frame by frame
        #     ret, frame = vid.read()
        #     if ret == True:
        #         cv2.imshow('frame', frame)
        #         #press q to exit
        #         if cv2.waitKey(25) & 0xFF == ord('q'):
        #             break
        #     else :
        #         break
        # vid.release()
        #
        # cv2.destroyAllWindows()











if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
