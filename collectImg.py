import cv2
import os
import datetime


if(__name__ == "__main__"):
    toggle = False

    capture = cv2.VideoCapture("rtsp://admin:ak@12345@192.168.0.106:554/Streaming/Channels/101")
    for name in os.listdir('./'):
        if(name.endswith(".jpg")):
            previousFrame = cv2.imread(name)
            previousFrame = cv2.cvtColor(previousFrame, cv2.COLOR_BGR2GRAY)
            toggle = True
            break
        
    if(toggle == False):
        ret, frame = capture.read()
        cv2.imwrite("previousFrame.jpg", frame) 
        previousFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
               
    # ret, frame = capture.read()
    threshold = 10000
    prev = datetime.datetime.now()
    while True:
        
        ret, frame = capture.read()
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        diff = cv2.absdiff(grayFrame, previousFrame)
        _, thresholded = cv2.threshold(diff, 110, 255, cv2.THRESH_BINARY)

        # Display the difference image
        num_differences = cv2.countNonZero(thresholded)
        print(f'Number of differences: {num_differences}')
        # cv2.imshow("threshold", thresholded)
        if(num_differences > threshold):
            
            duration = datetime.datetime.now() - prev
            print(duration.seconds)
            if(duration.seconds > 60):
                print(f'Number of differences: {num_differences}')
                cv2.imshow("diff", frame)
                prev = datetime.datetime.now()
        else:
            prev = datetime.datetime.now()
            cv2.destroyAllWindows()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()