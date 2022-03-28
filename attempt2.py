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

    # allow user to save the labeled video (checkbox)
    save_img = st.sidebar.checkbox("Save Video")

    # allow user to upload a video
    video_file_buffer = st.sidebar.file_uploader("Upload a Video", type = ["mp4", "mov", "avi", "asf", "m4v"])

    # display a demo video at first
    demo_video = "Bob_and_aws.mov"
    tfflie = tempfile.NamedTemporaryFile(suffix = "mp4", delete = False)

    # get input video
    if not video_file_buffer:
        vid = cv2.VideoCapture(demo_video)
        tfflie.name = demo_video
        dem_vid = open(tfflie.name, "rb")
        demo_bytes = dem_vid.read()

        st.sidebar.text("Input Video")
        st.sidebar.video(demo_bytes)
    else:
        tfflie.write(video_file_buffer.read())
        dem_vid = open(tfflie.name, "rb")
        demo_bytes = dem_vid.read()

        st.sidebar.text("Input Video")
        st.sidebar.video(demo_bytes)

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

    ret, first_frame = vid.read()
    # Scale and resize image
    resize_dim = 300
    max_dim = max(first_frame.shape)
    scale = resize_dim/max_dim
    first_frame = cv2.resize(first_frame, None, fx=scale, fy=scale)
    # Convert to gray scale
    prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)


    # Create mask
    mask = np.zeros_like(first_frame)
    # Sets image saturation to maximum
    mask[..., 1] = 255


    # out = cv2.VideoWriter('video.mp4',-1,1,(600, 600))

    while(vid.isOpened()):
        # Read a frame from video
        ret, frame = vid.read()

        # Convert new frame format`s to gray scale and resize gray frame obtained
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=scale, fy=scale)
            #blur???
        #gray = cv2.GaussianBlur(gray, (5, 5), 0)
        gray = cv2.GaussianBlur(gray,(21,21),cv2.BORDER_DEFAULT)

            #bllur

        #blur

        # Calculate dense optical flow by Farneback method
        # https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowfarneback
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, pyr_scale = 0.5, levels = 5, winsize = 11, iterations = 5, poly_n = 5, poly_sigma = 1.1, flags = 0)
        # Compute the magnitude and angle of the 2D vectors
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        # Set image hue according to the optical flow direction
        mask[..., 0] = angle * 180 / np.pi / 2
        # Set image value according to the optical flow magnitude (normalized)
        mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        # Convert HSV to RGB (BGR) color representation
        rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)

        # Resize frame size to match dimensions
        frame = cv2.resize(frame, None, fx=scale, fy=scale)




        # Open a new window and displays the output frame
        dense_flow = cv2.addWeighted(frame, 1,rgb, 2, 0)
        cv2.imshow("Dense optical flow", dense_flow)
        # out.write(dense_flow)
        # Update previous frame
        prev_gray = gray
        # Frame are read by intervals of 1 millisecond. The programs breaks out of the while loop when the user presses the 'q' key
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    # The following frees up resources and closes all windows
    vid.release()

    cv2.destroyAllWindows()



if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
