#!/usr/bin/env python
import argparse
import os
import cv2
import numpy as np
import os.path as osp
from glob import glob
from Flow import Flow


def cvReadImg(img_path):
    return cv2.imread(img_path).astype(np.float32)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir')
    parser.add_argument('save_dir')
    parser.add_argument('--show', type=bool, default=False, help='Shows optical flow while processing')
    args = parser.parse_args()

    flow_x_list = sorted(glob(osp.join(args.input_dir, 'flow_x_*.jpg')))
    flow_y_list = sorted(glob(osp.join(args.input_dir, 'flow_y_*.jpg')))

    bound = 20 #Farnback was calculated with this value
    flow = Flow()

    for idx, x_path, y_path in zip(range(1, len(flow_x_list)+1), flow_x_list, flow_y_list):
        x_img = cvReadImg(x_path)[..., 0]
        y_img = cvReadImg(y_path)[..., 0]
        h, w = x_img.shape[:2]

        nnf = np.zeros((h,w,2), dtype=np.float32)
        nnf[..., 0] = ((x_img / 255.) * 2 * bound) - bound
        nnf[..., 1] = ((y_img / 255.) * 2 * bound) - bound

        color_map = flow.visualize(nnf) * 255.
        cv2.imwrite(os.path.join(args.save_dir, '%06d.png'%idx), color_map)

        if args.show:
            cv2.imshow("colored flow", color_map)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
