
import cv2
import numpy as np

uploaded_vid = cv2.VideoCapture('Bob_and_aws.mov')

while(uploaded_vid.isOpened()):
    # capture frame by frame
    ret, frame = uploaded_vid.read()
    if ret == True:
        # TO-DO: DISPLAY IN UI, NOT IN OUTSIDE WINDOW 
        cv2.imshow('frame', frame)
        #press q to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else :
        break
uploaded_vid.release()

cv2.destroyAllWindows()
