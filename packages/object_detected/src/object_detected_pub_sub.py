#!/usr/bin/env python3

import os
import rospy
import cv2

from datetime import datetime

from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage

import torch

import sys
import os
from pathlib import Path

from duckietown.dtros import DTROS, NodeType
# from duckietown.dtros import DTROS, NodeType

"""

"""
class ObjectDetector(DTROS):

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(ObjectDetector, self).__init__(node_name=node_name, node_type=NodeType.PERCEPTION)
        # construct publisher
        self.ann_img_pub = rospy.Publisher('IsAlive', CompressedImage, queue_size=10)
        self.bounding_box_pub = rospy.Publisher('object_detected', String, queue_size=10)
        self.coord_pub = rospy.Publisher('')
        self.node_name=node_name
        self.node_type=NodeType.PERCEPTION
        self.veh_name = rospy.get_namespace().strip("/")
        self.message = "Hello World!"


        self.trained_model = torch.hub.load('./', 'custom', path='./weights/best.pt', source='local', force_reload=True)
        self.trained_model.conf = 0.621
        
        self.img = None
        
        # get image from ROS
        self.img_subscriber = rospy.Subscriber(self.veh_name + "/hostname/camera_node/image/compressed", CompressedImage, self.callback)
        
        self.bridge = CvBridge()
        
        
    def do_obj_detection(self, cv_image):
        
        pred_list = self.trained_model()
        
        for pred in pred_list:
            x_topleft = (int(pred[0]), int(pred[1]))
            x_botright = (int(pred[2]), int(pred[3]))
            conf = pred[4]
            classes = results.names
            obj_class = classes[int(pred[5])]

            im_ann = cv2.rectangle(im, x_topleft, x_botright, color=(255, 0, 0), thickness=4)
            im_ann = cv2.putText(im_ann, f"{obj_class}: {conf}", x_topleft, color=(255, 0, 0), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1)
            
            msg = self.bridge.cv2_to_compressed_imgmsg(im_ann)
            msg.header.stamp = rospy.get_rostime()
            self.ann_img_pub.publish(msg)
        return (f'{obj_class} {x_topleft} {x_botright} {conf}')
        
        
    
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
        
        self.do_obj_detection(self, cv_image)

if __name__ == '__main__':
    # create the node
    node = ObjectDetector(node_name='object_detector')
    # run node
    node.run()
    # keep spinning
    rospy.spin()