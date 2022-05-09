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
    kpi1, kpi2, kpi3 = st.columns(3)

    # initialize column values
    with kpi1:
        st.markdown("**Frame Rate**")
        kpi1_text = st.markdown("0")
    with kpi2:
        st.markdown("**Tracked Objects**")
        kpi2_text = st.markdown("0")
    with kpi3:
        st.markdown("**Width**")
        kpi3_text = st.markdown("0")

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
        # adds a start button and only plays the video if pressed
        if st.button("Start Video"):
            # TO-DO:
            # input: interval, number of crabs
            # make it so you can't change those after the video starts
            # make a terminal to write to while video is playing (UI)
            # cv2.imshow("Dense optical flow", dense_flow)
            # out.write(dense_flow)
            # Update previous frame
            # COMMENTED THIS OUT
            # prev_gray = gray
            # # Frame are read by intervals of 1 millisecond. The programs breaks out of the while loop when the user presses the 'q' key
            # if cv2.waitKey(10) & 0xFF == ord('q'):
            #     break
            tfflie.write(video_file_buffer.read())

        vid = cv2.VideoCapture(tfflie.name)
        while(vid.isOpened()):
            # capture frame by frame
            ret, frame = vid.read()
            if ret == True:
                cv2.imshow('frame', frame)
                #press q to exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else :
                break
        vid.release()

        cv2.destroyAllWindows()











if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
