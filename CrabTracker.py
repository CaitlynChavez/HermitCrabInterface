#https://www.pyimagesearch.com/2018/08/06/tracking-multiple-objects-with-opencv/
#Tracking multiple objects with OpenCV
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


distance_threshold = 1
frames_to_average = 10 #Averages the last x frames for smoothing out coordinate/tracking accuracy
frame_lap_threshold = 120 #used for lap analysis, a minimum of 120 frames is required per lap to ensure laps aren't counted multiple times
total_frames = 0
cup_ratio = 1
fps = 1
length_average_box_side = 0
# start_stop_threshold = 45 #threshold for frames needed to count as moving or not moving


#contains information for crab box label including name, distance moved, and last known coordinate
class BoxInfo(object):
    def __init__(self, name):

        self.name = name
        self.distance_moved = 0
        self.old_coord = (-1,-1)
        self.start_coord = (-1,-1)
        self.number_of_laps = 0
        self.lap_timer = 0
        self.lap_distance = 0
        self.waiting_time = 0
        self.coordQueue = []

        self.current_minute_distance = 0
        self.minute_distance_list = []
        self.minute_total_distance_list = []
        self.current_minute_timer = 0
        self.current_minute_wait_time = 0
        self.minute_wait_over_time_list = []

        self.minute_total_laps_list = []

        self.movingCounter = 0

    def updateCoord(self, coord):
        global fps
        if self.lap_timer > 0:
            self.lap_timer-= 1
        new_coord = coord
        self.coordQueue.insert(0, new_coord)
        if len(self.coordQueue) > frames_to_average:
            self.coordQueue.pop()
        #print(self.coordQueue)

        x_sum = 0
        y_sum = 0
        for i in range(0, len(self.coordQueue)):
            x_sum += self.coordQueue[i][0]
            y_sum += self.coordQueue[i][1]
        new_coord = ((x_sum/len(self.coordQueue)), (y_sum/len(self.coordQueue)) )

        #checks for first time to make sure it has a proper coordinate
        if self.old_coord != (-1,-1):
            wait_distance_threshold = distance_threshold*.7
            new_distance = self.calcDistance(self.old_coord, new_coord)
            #threhold for adding new distance (to avoid adding distance while waiting)
            # print("is wait working:", new_distance, wait_distance_threshold)
            if new_distance >= distance_threshold:
                global cup_ratio
                #moving

                self.distance_moved+= (new_distance*cup_ratio)
                self.current_minute_distance+= (new_distance*cup_ratio)
                self.old_coord = new_coord
                self.lap_distance+=new_distance
            #not moving, checks if the movement is smaller than a threshold to count as wait
            elif new_distance < (wait_distance_threshold):
                self.waiting_time +=1
                self.current_minute_wait_time+=1

            if total_frames%frames_per_minute == 0:
                self.minute_distance_list.append(self.current_minute_distance)
                self.current_minute_distance = 0

                self.minute_total_distance_list.append(self.distance_moved)

                self.minute_total_laps_list.append(self.number_of_laps)

                self.minute_wait_over_time_list.append(self.current_minute_wait_time/fps)
                self.current_minute_wait_time = 0
        else:#first coordinate put in, sets it up
            self.old_coord = new_coord
            self.start_coords = new_coord
            self.lap_timer = frame_lap_threshold

    def checkLaps(self, coord):
        lap_marker_distance = self.calcDistance(coord, self.start_coords)
        if self.lap_timer == 0 and lap_marker_distance < length_average_box_side*.5 and self.lap_distance > length_average_box_side*3.5:
            self.number_of_laps+=1
            self.lap_timer = frame_lap_threshold
            self.lap_distance = 0
    def returnBoxInfo(self):
        global fps
        return self.name, self.distance_moved, float(self.waiting_time)/fps
    def returnBoxMinuteLists(self):
        return self.minute_distance_list, self.minute_wait_over_time_list, self.minute_total_distance_list, self.minute_total_laps_list
    def printBoxInfo(self):
        global fps
        print("name:", self.name, " distance:", self.distance_moved, "cm # of laps:", self.number_of_laps, " waiting time", self.waiting_time/fps)
    def returnCSVData(self):
        outputList = [self.name, ""]
        outputList.extend(self.minute_distance_list)
        outputList.extend(self.minute_total_distance_list)
        outputList.extend(self.minute_total_laps_list)
        return outputList
    #calculates distance between two coordinates
    def calcDistance(self, old_coord, new_coord):
        x1 = old_coord[0]
        y1 = old_coord[1]
        x2 = new_coord[0]
        y2 = new_coord[1]
        dx = abs(x2-x1)
        dy = abs(y2-y1)
        distance = math.sqrt(dx**2 + dy**2)
        return distance

class CrabTracker:
    def __init__(self, number_of_crabs_to_track, write_to_excel, write_to_video, video, video_name):
        print("Creating new instance of crab tracker")
        self.number_of_crabs_to_track = number_of_crabs_to_track
        self.write_to_excel = write_to_excel
        self.write_to_video = write_to_video
        self.crabVid = video
        self.video_name = video_name
        # self.total_frames = 0



        # self.distance_threshold = 0
        # self.length_average_box_side = 0

        self.cup_height = 0
        self.cup_width = 0

        self.cup_size = 11.5 #11.5 cm
        self.cup_average = 1




        self.BoxInfoList = []
        self.time_date = time.strftime("%d-%m-%Y-%H_%M_%S", time.localtime())


        self.trackers = cv2.MultiTracker_create()
        self.tracker_type = "csrt"

        self.apply_contrast = False
        self.v_contrast = 5#45
        self.resize = True

        frames_per_minute = -1 #frames per minute

        self.OPENCV_OBJECT_TRACKERS = {
            "csrt": cv2.TrackerCSRT_create,
            "kcf": cv2.TrackerKCF_create,
            "boosting": cv2.TrackerBoosting_create,
            "mil": cv2.TrackerMIL_create,
            "tld": cv2.TrackerTLD_create,
            "medianflow": cv2.TrackerMedianFlow_create,
            "mosse": cv2.TrackerMOSSE_create
        }



    #creates video_files folder if it is not present
    if not os.path.exists("video_files"):
        print("Folder for video_files created")
        os.makedirs("video_files")

    #creates video_files folder if it is not present
    if not os.path.exists("tracking_videos"):
        print("Folder for tracking_videos created")
        os.makedirs("tracking_videos")

    if not os.path.exists("excel_files"):
        print("Folder for excel_files created")
        os.makedirs("excel_files")


    #https://learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/
    #writing video
    #https://learnopencv.com/reading-and-writing-videos-using-opencv/
    #reads directory for files and displays files on screen

    def ExportMLInformationCSV(self, csvFileName):
        with open(csvFileName+'.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            box_list_length = len(self.BoxInfoList)
            if len(self.BoxInfoList) > 0:
                first_minute_list, junk, junk2, junk3 = BoxInfoList[0].returnBoxMinuteLists()
            num_minutes = len(first_minute_list)


            header_list= ["Animal", "Target"]
            dist_min_list = []
            total_dist_list = []
            total_lap_list = []

            for i in range(0, num_minutes):
                dist_min_list.append("min" + str(i+1) + "_dist/min")
                total_dist_list.append("min" + str(i+1) + "_total_dist/min")
                total_lap_list.append("min" + str(i+1) + "_total_laps")

            header_list.extend(dist_min_list)
            header_list.extend(total_dist_list)
            header_list.extend(total_lap_list)

            writer.writerow(header_list)

            for box_num in range(0, box_list_length):
                box_data = BoxInfoList[box_num].returnCSVData()
                writer.writerow(box_data)
            print("File written to", csvFileName+'.csv')






    def apply_brightness_contrast(self, input_img, brightness = 0, contrast = 0):

        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + brightness
            alpha_b = (highlight - shadow)/255
            gamma_b = shadow

            buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
        else:
            buf = input_img.copy()

        if contrast != 0:
            f = 131*(contrast + 127)/(127*(131-contrast))
            alpha_c = f
            gamma_c = 127*(1-f)

            buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

        return buf
# video_bool = True
# video_path, video_name = readVideoDirectoryForVideo()
# print(video_path)
# crabVid = cv2.VideoCapture(video_path)
# OpenCV object tracker implementations  #KCF, fast acc, csrt, most accurate but slower, mosse fast but inaccurate
# number_of_crabs_to_track = int(input("Please enter number of crabs to track:\n"))
    def startAnalyzingVideo(self):
        if not self.crabVid.isOpened():
            print("Video cannot be opened")
            sys.exit()
        resize_dim = 800
        ret, first_frame = self.crabVid.read()
        max_dim = max(first_frame.shape)
        scale = resize_dim/max_dim

        # Read first frame.
        ok, frame = self.crabVid.read()

        if not ok:
            print('Cannot read video file')
            sys.exit()
        global fps
        fps = self.crabVid.get(5)
        global frames_per_minute

        frames_per_minute = int(fps*60)
        print('Frames per second : ', fps,'FPS')
        frame = cv2.resize(frame, None, fx=scale, fy=scale)
        frame_height, frame_width = frame.shape[:2]
        frame_size = (frame_width, frame_height)

        #used to create output for mp4
        #out = cv2.VideoWriter('video_output.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), fps, (frame_width,frame_height))
        #creates video output
        video_output = cv2.VideoWriter('tracking_videos/' + self.video_name+self.time_date+".avi", cv2.VideoWriter_fourcc('M','J','P','G'), 40, frame_size)

        # loop over frames from the video stream
        print_threshold = int(fps) #how often to print info to screen by default set to 1s
        print_counter = 0
        find_cup_size = True

        cupWidth = 1
        cupHeight = 1
        #while video is running
        while True:
            # grab the current frame, then handle if we are using a
            # VideoStream or VideoCapture object
            ok, frame = self.crabVid.read()

            if not ok:
                break

            if self.resize == True:
                frame = cv2.resize(frame, None, fx=scale, fy=scale)
            if (self.apply_contrast):
                frame = apply_brightness_contrast(frame, brightness = 0, contrast=v_contrast)

            #updates all trackers
            # grab the updated bounding box coordinates (if any) for each
            # object that is being tracked
            (success, boxes) = self.trackers.update(frame)


            # loop over the bounding boxes and draw then on the frame
            iterator = 0

            if find_cup_size == True:
                print("\nPlease put a bounding box over a cup")
                box = cv2.selectROI("Frame", frame, fromCenter=False,
                showCrosshair=True)
                (x, y, w, h) = [int(v) for v in box]
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # x_mid = (x + x + w)/2
                # y_mid = (y + y + h)/2
                self.cup_width = abs(w)
                self.cup_height = abs(h)

                self.cup_average = (self.cup_width + self.cup_height)/2
                global cup_ratio
                cup_ratio = (self.cup_size/self.cup_average)
                print("cup width", self.cup_width, "cup height", self.cup_height, "cup average", self.cup_average, "cup ratio to cm", cup_ratio)


                find_cup_size = False
                print("\nNow label the crabs")


            for box in boxes:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                x_mid = (x + x + w)/2
                y_mid = (y + y + h)/2
                new_coord = (x_mid, y_mid)
                self.BoxInfoList[iterator].updateCoord(new_coord) #updates coordinate of each labeled box
                self.BoxInfoList[iterator].checkLaps(new_coord)
                iterator +=1

            #writes file
            if self.write_to_video == True:
              video_output.write(frame)
            # show the output frame
            cv2.imshow("Frame", frame)

            key = cv2.waitKey(1) & 0xFF
            #while loop for number of crabs to track
            while self.number_of_crabs_to_track > 0:
                if key == ord("q"):
                    number_of_crabs_to_track = 0
                    break
                box = cv2.selectROI("Frame", frame, fromCenter=False,
                showCrosshair=True)
                # create a new object tracker for the bounding box and add it
                # to our multi-object tracker
                tracker = self.OPENCV_OBJECT_TRACKERS[self.tracker_type]()
                self.trackers.add(tracker, frame, box)
                label_name = input("Please enter name of label:\n")
                if label_name == "quit" or label_name == "q":
                    self.number_of_crabs_to_track = 0
                    break
                self.BoxInfoList.append(BoxInfo(label_name)) #adds info for new box
                self.number_of_crabs_to_track = self.number_of_crabs_to_track -1


            global total_frames

            total_frames += 1
            #every time print counter = print_threshold so every 1 second print the info
            print_counter +=1
            if print_counter == print_threshold:
                print_counter =0
                print("Time =", int(total_frames/fps)+1, "seconds, frames:", total_frames)
                for i in range(0, len(self.BoxInfoList)):
                    self.BoxInfoList[i].printBoxInfo()


            #creates a distance threshold for moving crabVid waiting on first run
            if distance_threshold == 0:
              temp_distance_list = []
              sum = 0.0
              for box in boxes:
                  (x, y, w, h) = [int(v) for v in box]
                  xdist = abs(w)
                  ydist = abs(h)
                  print("xwidth:", xdist)
                  print("yheight", ydist)
                  temp_distance_list.append(xdist)
                  temp_distance_list.append(ydist)
              for i in range(0, len(temp_distance_list)):
                  sum += temp_distance_list[i]
              if len(temp_distance_list) != 0:
                average = sum/len(temp_distance_list)
                length_average_box_side = average
                print("final average", average)
                self.distance_threshold = average*0.06 #was 0.06
                if self.distance_threshold < 1:
                    self.distance_threshold = 1.2
                print("distance_threshold", self.distance_threshold)



            #if s key is selected, makes another bounding box
            if key == ord("s"):
                # select the bounding box of the object we want to track (make
                # sure you press ENTER or SPACE after selecting the ROI)
                box = cv2.selectROI("Frame", frame, fromCenter=False,
                showCrosshair=True)
                # create a new object tracker for the bounding box and add it
                # to our multi-object tracker
                tracker = OPENCV_OBJECT_TRACKERS[tracker_type]()
                self.trackers.add(tracker, frame, box)
                label_name  = input("Please enter name of label:\n")
                self.BoxInfoList.append(BoxInfo(label_name)) #adds info for new label box
                # if the `q` key was pressed, break from the loop
            elif key == ord("q"):
                break

        #once finished
        self.crabVid.release()
        if self.write_to_video == True:
          video_output.release()
          print("Labelled video recorded to", self.video_name)
        # ExportExcel(video_name)
        # ExportMinuteInformationExcel(video_name)
        self.ExportMLInformationCSV(self.video_name)
        self.total_time = total_frames/fps
        print("Video time:", total_time, "seconds with", total_frames, "frames" )
        print("cup size in pixels", cup_average, "cup ratio was ", cup_ratio)

        # close all windows
        cv2.destroyAllWindows()

# #def __init__(self, number_of_crabs_to_track, write_to_excel, write_to_video, video):
# print("start")
# vs = cv2.VideoCapture('Bob_and_aws.mov')
# crabTrack = CrabTracker(2,True,True,vs,"EXAMPLEOUTPUT")
# crabTrack.startAnalyzingVideo()
# print("end")
