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
    demo_video = "Light_cropped_HCJan_20_2022.mp4"
    tfflie = tempfile.NamedTemporaryFile(suffix = "mp4", delete = False)

    # get input video
    if not video_file_buffer:
        vid = cv2.VideoCapture(demo_video)
        tfflie.name = demo_video
        dem_vid = open(tifflie.name, "rb")
        demo_bytes = dem_vid.read()

        st.sidebar.text("Input Video")
        st.sidebar.video(demo_bytes)
    else:
        tfflie.write(video_file_buffer.read())
        dem_vid = open(tifflie.name, "rb")
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

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
