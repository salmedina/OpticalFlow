from Flow import Flow
from glob import glob
import os.path as osp
import cv2
import os

def get_filename(file_path):
    return osp.splitext(osp.basename(flo_path))[0]

if __name__=='__main__':
    flo_dir = '/mnt/Alfheim/Data/DIVA_Proposals/optical_flow/pwcnet/VIRAT_S_000005_100'
    hsv_dir = '/mnt/Alfheim/Data/DIVA_Proposals/hsv/pwcnet/VIRAT_S_000005_100/'
    flo_path_list = sorted(glob(osp.join(flo_dir, '*.flo')))
    flow = Flow()

    for flo_path in flo_path_list:
        nnf = flow.read(flo_path)
        color_map = flow.visualize(nnf) * 255.
        cv2.imwrite(osp.join(hsv_dir, '%s.png'%get_filename(flo_path)), color_map)
