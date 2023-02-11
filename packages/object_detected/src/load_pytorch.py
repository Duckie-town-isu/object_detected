import os
import sys
from pathlib import Path

import torch
import cv2
# import torchvision

from utils.plots import Annotator
from utils.general import scale_boxes

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

if __name__ == '__main__':
    # before run the next line, go to hugconf.py and change the class num as your model specified
    # also save the best.pt and best.yaml under the same folder
    model = torch.hub.load('./', 'custom', path='./weights/best.pt', source='local', force_reload=True)
    model.conf = 0.621

    dataPath = os.listdir('../Pictures')

    results = model(dataPath)
    results.show()

#     predictions = (results.pred[0]).tolist()
#
#     print(predictions)
#
#     im = cv2.imread(dataPath)
#     cv2.imshow("Name", im)
#     cv2.waitKey(5000)
#
# # yolo output is xyxy x_low y_low,
#
#
#     if len(predictions) != 0:
#         for i, det in enumerate(predictions):  # per image
#             print(det)
#             x_topleft = (int(det[0]), int(det[2]))
#             x_botright = (int(det[1]), int(det[3]))
#             conf = det[4]
#             classes = results.names
#             obj_class = classes[int(det[5])]
#             im_ann = cv2.rectangle(im, x_topleft, x_botright, color=(255, 0, 0))
#             im_ann = cv2.putText(im_ann, f"{obj_class}: {det[4]}", x_topleft, color=(255, 0, 0), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=10)
#
#         cv2.imshow("Name", im_ann)
#         cv2.waitkey(1000)

