import cv2import resnet as rimport numpy as npimport tensorflow as tffrom imutils.object_detection import non_max_suppressionimport roslibimport rospyimport sysfrom sensor_msgs.msg import Imagefrom std_msgs.msg import Int16, Float64, Stringfrom cv_bridge import CvBridgeimport loggingimport osfrom nets import resnet_v2from preprocessing import inception_preprocessingimport timebbox_list = []class EmotionClassifier():    def __init__(self):        slim = tf.contrib.slim        CLASSES = ['anger', ' happy ', 'neutral', ' sad ', 'surprise']        image_size = 160        checkpoints_dir = 'models/inception_5/'        logging.basicConfig(filename='result.log', filemode='w', level=logging.INFO)        self.logger = logging.getLogger('emotion classifier')        # loading model        with tf.Graph().as_default():            self.image = tf.placeholder(tf.uint8, [None, None, 3])            self.processed_image = inception_preprocessing.preprocess_image(self.image, image_size, image_size, is_training=False)            self.processed_images = tf.placeholder(tf.float32, [None, image_size, image_size, 3])            with slim.arg_scope(resnet_v2.resnet_arg_scope()):                logits, _ = resnet_v2.resnet_v2_50(self.processed_images, num_classes=len(CLASSES), is_training=False)                self.probs = tf.nn.softmax(logits)            init_fn = slim.assign_from_checkpoint_fn(                os.path.join(checkpoints_dir, 'model.ckpt-60000'),                slim.get_model_variables('resnet_v2_50'))            config = tf.ConfigProto()            config.gpu_options.allow_growth = True            config.allow_soft_placement = True            self.sess = tf.Session(config=config)            init_fn(self.sess)class RosTensorFlow():        def __init__(self):        self.bridge = CvBridge()        self._sub = rospy.Subscriber('CVsub', Image, self.callback, queue_size=1, buff_size = 52428800)        self._pub = rospy.Publisher('CVpub', Image, queue_size=1)        self._pub1 = rospy.Publisher('result', String, queue_size=1)        self._pubBody = rospy.Publisher('result_Body', String, queue_size=1)	self.emoC1 = EmotionClassifier()        print("------Initial Entry Point of Emotion Detecting , Starting now ......")        # --------------------------------- 	    def callback(self, image_msg):        face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_alt.xml')        # camera = cv2.VideoCapture(0)        # initialize the HOG descriptor/person detector        hog = cv2.HOGDescriptor()        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())        while (True):            # ret, frame = camera.read()            frame = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")            imageBody = frame            # detect people in the image            (rects, weights) = hog.detectMultiScale(imageBody, winStride=(4, 4), padding=(8, 8), scale=1.3)            rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])            pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)            # draw the final bounding boxes            for (xA, yA, xB, yB) in pick:                cv2.rectangle(imageBody, (xA, yA), (xB, yB), (0, 255, 0), 2)                bbox_list = [(xA, yA, xB, yB)]                print ("----body coordinator : ",bbox_list )                ansBody = str(bbox_list)                ansBody2 = ":" + str(bbox_list)                # print('----', bbox_list[idx], "===", idx, fexpr_list[idx][0],fexpr_list[idx][1])                ## ============================================================                rospy.logout("---------------Detecting Face Loop Starting ----------------------------")                rospy.loginfo("-----------Body :" +  (ansBody) + ansBody2)                self._pubBody.publish("bodyCoor :" +  (ansBody) + ansBody2)            image = frame            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)            faces = face_cascade.detectMultiScale(                gray,                scaleFactor=1.3,                minNeighbors=5)            bbox_list = [(x, y, w, h) for (x, y, w, h) in faces]            print("\n","----Return Face Coordinator ......... : ", bbox_list,"\n")            #fexpr_list = r.classify_image(image, bbox_list)            #fexpr_list = [(2, 0.99), (1,0.98)]            fexpr_list = r.classify_image(self.emoC1.sess, self.emoC1.image, self.emoC1.processed_image, self.emoC1.processed_images, self.emoC1.probs, self.emoC1.logger,image, bbox_list)             for idx,bbox in  enumerate(bbox_list): 		pos = (bbox[0],bbox[1])                xx = bbox[0]                yy = bbox[1]                wd = bbox[2]                ht = bbox[3]                 answer = fexpr_list[idx][0]                answer1 = str(fexpr_list[idx][1])                answer2 = ":" + str(bbox_list[idx])                # print('----', bbox_list[idx], "===", idx, fexpr_list[idx][0],fexpr_list[idx][1])                ## ============================================================                rospy.logout("---------------Detecting Face Loop Starting ----------------------------")                if (answer == 0):                    rospy.loginfo("-----------Anger :" + answer1 + answer2)                    self._pub1.publish("Anger :" + answer1 + answer2)                elif (answer == 1):                    rospy.loginfo("---------Happy :" + answer1 + answer2)                    self._pub1.publish("Happy :" + answer1 + answer2)                elif (answer == 2):                    rospy.loginfo("-------- Neutral :" + answer1 + answer2)                    self._pub1.publish("Neutral :" + answer1 + answer2)                elif (answer == 3):                    rospy.loginfo("-------- Sad :" + answer1 + answer2)                    self._pub1.publish("Sad :" + answer1 + answer2)                else:                    rospy.loginfo("----------------unkwone  emotion :" + answer1 + answer2)                    self._pub1.publish("unkwone  emotion :" + answer1 + answer2)                r.draw_label(image, answer, pos, wd, ht)                #cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)                cv2.rectangle(image, pos , (xx + wd, yy + ht), (0, 0, 255), 2)            # cv2.imshow('final', image)            cv2.imwrite("body.jpg", image)            msg = self.bridge.cv2_to_imgmsg(image, "bgr8")            self._pub.publish(msg)            break         cv2.destroyAllWindows()        print("---------------Detecting Loop Ending .............................")    def main(self):        rospy.spin()        print("------Braking Program by User .................")if __name__ == "__main__":    rospy.init_node('rostensorflow')    tensor = RosTensorFlow()    tensor.__init__()    tensor.main()