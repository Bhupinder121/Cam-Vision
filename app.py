import cv2
from flask import Flask, render_template, request, Response
import os



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route("/check")
def check():
    print("connection")
    # return render_template('index.html')
    return "hello243432"



def gen():
    # Open the RTSP stream
    cap = cv2.VideoCapture("rtsp://admin:ak@12345@192.168.0.106:554/Streaming/Channels/101")
    
    ret, frame = cap.read()
    previousFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    while True:
        # Read frame from stream
        ret, frame = cap.read()
        if(isinstance(frame, type(None)) == True):
            capture = cv2.VideoCapture("rtsp://admin:ak@12345@192.168.0.106:554/Streaming/Channels/101")
            ret, frame = capture.read()

        # ret, normal_jpeg = cv2.imencode('.jpg', frame)
        # camFrame = (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + normal_jpeg.tobytes() + b'\r\n')
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        

        diff = cv2.absdiff(frame, previousFrame)
        # num_differences = cv2.c
        # Encode the frame in JPEG format
        ret, jpeg = cv2.imencode('.jpg', diff)

        filerFrame = (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

        yield filerFrame
        # Yield the frame to the client
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    print("got it!!")
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # thread = threading.Thread(target=gen)
    # thread.start()
    app.run(host="0.0.0.0")
    