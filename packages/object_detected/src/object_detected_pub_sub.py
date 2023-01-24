#!/usr/bin/env python3

import os
import rospy
import cv2

from datetime import datetime

from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage

import torch

from duckietown.dtros import DTROS, NodeType
# from duckietown.dtros import DTROS, NodeType

"""

"""
class ObjectDetector(DTROS):

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(ObjectDetector, self).__init__(node_name=node_name, node_type=NodeType.PERCEPTION)
        # construct publisher
        self.pub = rospy.Publisher('IsAlive', String, queue_size=10)
        self.pub = rospy.Publisher('object_detected', String, queue_size=10)
        self.coord_pub = rospy.Publisher('')
        self.node_name=node_name
        self.node_type=NodeType.PERCEPTION
        self.veh_name = rospy.get_namespace().strip("/")
        self.message = "Hello World!"
        # self.trained_model = torch.load("trained_5m/weights/best.pt")
        self.trained_model = torch.hub.load('.', 'custom', path='/path/to/yolov5/runs/train/exp5/weights/best.pt', source='local') 
        self.trained_model.eval()
        
        self.img = None
        
        # get image from ROS
        self.img_subscriber = rospy.Subscriber(self.veh_name + "/hostname/camera_node/image/compressed", CompressedImage, self.callback)
        
    """
    Important websites
    https://learning.oreilly.com/library/view/ros-robotics-projects/9781783554713/ch07s05.html#ch07lvl2sec57
    https://github.com/OTL/rostensorflow
    https://subscription.packtpub.com/book/hardware-&-creative/9781783554713/7/ch07lvl1sec57/image-recognition-using-ros-and-tensorflow
    Make a publisher that publishes the class of the first object detected
    
    model = torch.hub.load('.', 'custom', path='/path/to/yolov5/runs/train/exp5/weights/best.pt', source='local') 
    """
    def do_obj_detection(self, cv_image):
        results = self.trained_model(cv_image)
        
        
    
    def run(self):
        # publish message every 1 second
        rate = rospy.Rate(1) # 1Hz
        while not rospy.is_shutdown():
            
            rospy.loginfo("Publishing message: '%s'" % self.message)
            self.pub.publish(self.message)        
            rate.sleep()
            
    def callback(self, data):
        
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(data.data, "bgr8")
        self.img = cv_image
        if not cv2.imwrite("Captured_image_" + datetime.now().strftime("%d/%m/%Y_%H:%M:%S"), cv_image):
            self.message = "IMWRITE FAILED"
            raise Exception("imwrite failed")
        
        do_obj_detection(self, cv_image)

if __name__ == '__main__':
    # create the node
    node = ObjectDetector(node_name='object_detector')
    # run node
    node.run()
    # keep spinning
    rospy.spin()