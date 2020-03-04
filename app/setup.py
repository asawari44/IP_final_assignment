import cv2
import os
def create_app():
  pathOut= "frames"
  global total_count
  vidcap = cv2.VideoCapture("../data/vehicle1.avi")
  total_count = 0
  while (vidcap.isOpened()):
      ret, frame= vidcap.read()

      if ret == True:
         print('Read %d frame: ' % total_count, ret)
         cv2.imwrite(os.path.join(pathOut, "frame{:d}.jpg".format(total_count)), frame)  # save frame as JPEG file
         total_count += 1
      else:
            break

    # When everything done, release the capture
  vidcap.release()
  cv2.destroyAllWindows()

create_app()
