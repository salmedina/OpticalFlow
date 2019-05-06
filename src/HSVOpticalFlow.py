#!/usr/bin/env python
import argparse
import glob
import os
import cv2
import numpy as np

def cvReadImg(img_path):
    return cv2.imread(img_path).astype(np.float32)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('flow_dir')
    parser.add_argument('save_dir')
    args = parser.parse_args()

    flow_path_list = glob.glob(os.path.join(args.flow_dir, '*'))

    for idx, flow_path in enumerate(flow_path_list):
        flow_img = cvReadImg(flow_path)
        # Use Hue, Saturation, Value colour model
        hsv = np.zeros(flow_img.shape, dtype=np.uint8)
        hsv[..., 1] = 255

        mag, ang = cv2.cartToPolar(flow_img[..., 0], flow_img[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        color_map = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        cv2.imwrite(os.path.join(args.save_dir, os.path.basename(flow_path)), color_map)
        cv2.imshow("colored flow", color_map)
        cv2.waitKey(0)
        cv2.destroyAllWindows()