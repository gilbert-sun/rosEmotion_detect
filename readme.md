
1.----------------------
source /root/catkin_ws/devel/setup.bash 
roscore


2.----------------------
source /root/catkin_ws/devel/setup.bash 
python main1.py CVsub:=image_raw 


3.----------------------
source /root/catkin_ws/devel/setup.bash 
rosrun libuvc_camera camera_node


4.----------------------
source /root/catkin_ws/devel/setup.bash 
rosrun image_view image_view image:=image_raw


5.----------------------
source /root/catkin_ws/devel/setup.bash 
rosrun image_view image_view image:=CVpub


6.----------------------
source /root/catkin_ws/devel/setup.bash 
rostopic echo /result


7.----------------------
source /root/catkin_ws/devel/setup.bash 
rosrun rqt_graph rqt_graph


