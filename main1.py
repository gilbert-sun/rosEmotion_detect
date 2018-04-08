import cv2
import resnet as r
import numpy as np
import tensorflow as tf
#from imutils.object_detection import non_max_suppression
import roslib
import rospy
import sys
from sensor_msgs.msg import Image
from std_msgs.msg import Int16, Float64,  String
from cv_bridge import CvBridge


bbox_list =[]


class RosTensorFlow():
    def __init__(self):

        self.bridge = CvBridge()

        self._sub = rospy.Subscriber('CVsub', Image, self.callback, queue_size=1) 

        self._pub = rospy.Publisher('CVpub',Image, queue_size=1)

	self._pub1 = rospy.Publisher('result',String, queue_size = 1)


        print("------111111111---")



    def callback(self, image_msg):
          face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_alt.xml')


          # camera = cv2.VideoCapture(0)
          while (True):
              # ret, frame = camera.read()
 
              frame = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")
              image =frame
              gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

              faces = face_cascade.detectMultiScale(
                  gray,
                  scaleFactor=1.3,
                  minNeighbors=5)


              bbox_list = [(x, y, w, h) for (x, y, w, h) in faces]
              print("\n\n-----------\n", bbox_list)

              fexpr_list = r.classify_image(image,bbox_list)
	      #fexpr_list = [(2, 0.99), (1,0.98)]
#

              #idx =0 
	      for idx in range(len(bbox_list)):
              #for (x, y, w, h) in faces:

		  #cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)

                  bbox = bbox_list[idx]

                  pos = (bbox[0], bbox[1])
                  xx = bbox[0]
                  yy = bbox[1]
                  wd = bbox[2]
                  ht = bbox[3]
                  fexpr = fexpr_list[idx][0]
                  #fexpr = fexpr_list[idx][0]
                  answer = fexpr_list[idx][0]
		  answer1 = str(fexpr_list[idx][1])
		  answer2 = ":" + str(bbox_list[idx])

                  #print('----', bbox_list[idx], "===", idx, fexpr_list[idx][0],fexpr_list[idx][1]) 
   
              ## ============================================================
                  rospy.logout("--------------- HA HA ----------------------------")
                  if(answer == 0):
			rospy.loginfo("-----------Anger :"+ answer1+ answer2)
			self._pub1.publish("Anger :"+ answer1+ answer2)
		  elif(answer == 1):
			rospy.loginfo("---------Happy :"+ answer1+ answer2)
			self._pub1.publish("Happy :"+ answer1+ answer2)
		  elif(answer == 2):
			rospy.loginfo("-------- Neutral :"+ answer1+ answer2)
			self._pub1.publish("Neutral :"+ answer1+ answer2)
          	  elif(answer == 3):
			rospy.loginfo("-------- Sad :"+ answer1+ answer2)
			self._pub.publish("Sad :"+ answer1+ answer2)
		  else:
			rospy.loginfo("----------------unkwone  emotion :"+ answer1+ answer2)
			self._pub1.publish("unkwone  emotion :"+ answer1+ answer2)  
              ## ------------------------------------------------------------
                  r.draw_label(image, fexpr, pos, wd, ht)
		  cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
                  #cv2.rectangle(image, (xx, yy), (xx + wd, yy + ht), (0, 0, 255), 2)

              #cv2.imshow('final', image)
              cv2.imwrite("body.jpg", image)
              msg = self.bridge.cv2_to_imgmsg(image, "bgr8")
              self._pub.publish(msg)
              k = cv2.waitKey(30) & 0xff
	      k = True
              if k == 27 or k == True:
              	break
          # camera.release()
          cv2.destroyAllWindows()

          print("------0000000---")

    def main(self):
          rospy.spin()
          # face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_alt.xml')
          #
          #
          # camera = cv2.VideoCapture(1)
          # while (True):
          #     ret, frame = camera.read()
          #
          #     # image = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_CUBIC)
          #     #
          #     # # detect people in the image
          #     # (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.3)
          #     #
          #     # rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
          #     # pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
          #     #
          #     # # draw the final bounding boxes
          #     # for (xA, yA, xB, yB) in pick:
          #     #     cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
          #     image =frame
          #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
          #
          #     faces = face_cascade.detectMultiScale(
          #         gray,
          #         scaleFactor=1.3,
          #         minNeighbors=5,
          #         minSize=(30, 30),
          #         flags=cv2.CASCADE_SCALE_IMAGE)
          #
          #     # # ==============================
          #     #
          #     #
          #     # bbox_list = [(x, y, w, h) for (x, y, w, h) in faces]
          #     # print("\n\n-----------\n", bbox_list)
          #     #
          #     # fexpr_list = r.classify_image(image, bbox_list)
          #     #
          #     # for idx in range(len(bbox_list)):
          #     #     bbox = bbox_list[idx]
          #     #
          #     #     pos = (bbox[0], bbox[1])
          #     #     xx = bbox[0]
          #     #     yy = bbox[1]
          #     #     wd = bbox[2]
          #     #     ht = bbox[3]
          #     #     # fexpr = fexpr_list[idx]
          #     #     fexpr = fexpr_list[idx][0]
          #     #     print('----', bbox_list[idx], "===", idx, fexpr_list[idx][0],fexpr_list[idx][1])
          #     #
          #     #     answer = fexpr_list[idx][0]
          #     #     rospy.logout("-------------------------------------------")
          #     #     if(answer == 0):
          #     #       rospy.loginfo("Anger")
          #     #       self._pub.publish(0)
          #     #     elif(answer == 1):
          #     #       rospy.loginfo("Happy")
          #     #       self._pub.publish(1)
          #     #     elif(answer == 2):
          #     #       rospy.loginfo("Neutral")
          #     #       self._pub.publish(2)
          #     #     elif(answer == 3):
          #     #       rospy.loginfo("Sad")
          #     #       self._pub.publish(3)
          #     #     else:
          #     #       rospy.loginfo("unkwone  emotion")
          #     #       self._pub.publish(4)
          #     #
          #     #
          #     #     r.draw_label(image, fexpr, pos, wd, ht)
          #     #
          #     #     cv2.rectangle(image, (xx, yy), (xx + wd, yy + ht), (0, 0, 255), 2)
          #     #
          #     #     roi_gray = gray[yy:yy + ht, xx:xx + wd]
          #     #
          #     #     bbox_list = [(xx, yy, wd, ht)]
          #     #
          #     #     print("1", type(roi_gray))
          #     #     print("2", roi_gray.shape)
          #     #     print("3", roi_gray)
          #     #     print(bbox_list[0])
          #     #
          #     #     # ------------------------------------------------------------
          #     for (x, y, w, h) in faces:
          #         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
          #         # img = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
          #         # (x,y) , (x+w,y) ,(x+w,y+h),(x,y+h)
          #         roi_gray = gray[y:y + h, x:x + w]
          #         # horizontal_offset = 0.15 * w
          #         # vertical_offset = 0.2 * h
          #         # extracted_face = gray[y + vertical_offset:y + h,
          #         #                  x + horizontal_offset:x - horizontal_offset + w]
          #         bbox_list = [(x, y, w, h)]
          #         # print("-----------", (x,y) ,(x,y+h), (x+w,y+h),(x+w,y) )
          #         # print ( "=======",(x), (y),(w),(h) )
          #         print("1", type(roi_gray))
          #         print("2", roi_gray.shape)
          #         print("3", roi_gray)
          #         print(bbox_list[0])
          #     cv2.imshow('final', frame)
          #     cv2.imwrite("body.jpg", image)
          #
          #     k = cv2.waitKey(30) & 0xff
          #     if k == 27:
          #         break
          # camera.release()
          # cv2.destroyAllWindows()

          print("------333333333333---")

if __name__ == "__main__":
    rospy.init_node('rostensorflow')
    tensor = RosTensorFlow()
    tensor.main()

