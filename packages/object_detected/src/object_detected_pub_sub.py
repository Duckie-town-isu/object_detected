#!/usr/bin/env python3

import os
import rospy
import cv2

from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage

from duckietown.dtros import DTROS, NodeType


class ObjectDetector(DTROS):

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(ObjectDetector, self).__init__(node_name=node_name, node_type=NodeType.PERCEPTION)
        # construct publisher
        self.pub = rospy.Publisher('IsAlive', String, queue_size=10)
        self.pub = rospy.Publisher('Objects Detected', String, queue_size=10)
        self.node_name=node_name
        self.node_type=NodeType.PERCEPTION
        self.veh_name = rospy.get_namespace().strip("/")
        
        # get image from ROS
        self.ros_img = rospy.Subscriber(self.veh_name + "/hostname/camera_node/image/compressed", CompressedImage)
        

    def run(self):
        # publish message every 1 second
        rate = rospy.Rate(1) # 1Hz
        while not rospy.is_shutdown():
            message = "Hello World!"
            rospy.loginfo("Publishing message: '%s'" % message)
            self.pub.publish(message)
            
            bridge = CvBridge()
            cv_image = bridge.imgmsg_to_cv2(self.ros_img, desired_encoding='passthrough')
        
            cv2.imshow("Camera_image", cv_image)
        
            rate.sleep()

if __name__ == '__main__':
    # create the node
    node = ObjectDetector(node_name='object_detector')
    # run node
    node.run()
    # keep spinning
    rospy.spin()