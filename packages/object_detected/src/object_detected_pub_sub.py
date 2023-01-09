#!/usr/bin/env python3

import os
import rospy
import cv2

from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage

from duckietown.dtros import DTROS, NodeType

"""

"""
class ObjectDetector(DTROS):
    
    def do_obj_detectiom():
        pass

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(ObjectDetector, self).__init__(node_name=node_name, node_type=NodeType.PERCEPTION)
        # construct publisher
        self.pub = rospy.Publisher('IsAlive', String, queue_size=10)
        self.pub = rospy.Publisher('object_detected', String, queue_size=10)
        self.node_name=node_name
        self.node_type=NodeType.PERCEPTION
        self.veh_name = rospy.get_namespace().strip("/")
        
        self.img = None
        
        # get image from ROS
        self.img_subscriber = rospy.Subscriber(self.veh_name + "/hostname/camera_node/image/compressed", CompressedImage, self.callback)
        

    def run(self):
        # publish message every 1 second
        rate = rospy.Rate(1) # 1Hz
        while not rospy.is_shutdown():
            message = "Hello World!"
            rospy.loginfo("Publishing message: '%s'" % message)
            self.pub.publish(message)        
            rate.sleep()
            
    def callback(self, data):
        
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(data.data, "bgr8")
        cv2.imshow("Camera_image", cv_image)
        
        self.img = cv_image
        
        do_obj_detection(self, cv_image)

if __name__ == '__main__':
    # create the node
    node = ObjectDetector(node_name='object_detector')
    # run node
    node.run()
    # keep spinning
    rospy.spin()