import rospy
from darknet_ros_msgs.msg import BoundingBoxes
import time
from clientFlask1 import write_json_file_DayActivity, read_json_file_DayActivity,dayActivity_RepoFormat


def callback(msg):
    '''
    0 Class:
    1 "sitting"
    2 probability:
    3 0.845878005028
    4 xmin:
    5 46
    6 ymin:
    7 206
    8 xmax:
    9 573
    10 ymax:
    11 471
    '''
    boxMsg= str(msg.bounding_boxes[0]).split() #rospy.get_caller_id()   )
#    for idx in range(len(boxMsg)):
#	    print (idx, boxMsg[idx])

    json_data = read_json_file_DayActivity( "client_dayActivity.json")

# ['seq:', '11897', 'stamp:', 'secs:', '1545287058', 'nsecs:', '815070391', 'frame_id:', '"detection"']​
    headerTime = str(msg.header).split()[4]

    if(boxMsg[1] == "sitting"):
            json_data["sit_cum_time"] += 1
    elif(boxMsg[1] == "standing"):
            json_data["stand_cum_time"] += 1
    write_json_file_DayActivity("client_dayActivity.json",dayActivity_RepoFormat(json_data["sit_cum_time"], json_data["stand_cum_time"]))

    #print(write_json_file_DayActivity("client_dayActivity.json", dayActivity_RepoFormat(json_data["sit_cum_time"] , json_data["stand_cum_time"])))

    #rospy.loginfo(msg.bounding_boxes.xmin,msg.bounding_boxes.ymin,msg.bounding_boxes.xmax,msg.bounding_boxes.ymax)

def listener():

    rospy.init_node('subscribeDayActivity', anonymous=True)
    # print ("1",time.time())
    # print (time.strftime("%Y-%m-%d"))

    # subscribe and publish related topic
    rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, callback)

    #every 1 min to check activity status
    rospy.sleep(60)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()