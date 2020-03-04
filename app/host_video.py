#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import os,time
print(cv2.__version__)

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    pathOut= "frames"
    #os.mkdir(pathOut)
    vidcap = cv2.VideoCapture("../data/vehicle1.avi")
    count = 0
    while (vidcap.isOpened()):
      ret, frame= vidcap.read()

      if ret == True:
         print('Read %d frame: ' % count, ret)
         cv2.imwrite(os.path.join(pathOut, "frame{:d}.jpg".format(count)), frame)  # save frame as JPEG file
         jpeg_frame= open(pathOut+"/frame{:d}.jpg".format(count), "rb").read() 
         print("===========================")
         print(type(jpeg_frame))
         #ret, jpeg_frame = cv2.imencode(".jpg",frame)
         count += 1
         time.sleep(0.05)
         yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg_frame + b'\r\n')

      else:
            break
 
    # When everything done, release the capture
    vidcap.release()
    cv2.destroyAllWindows()
 
      
    
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
