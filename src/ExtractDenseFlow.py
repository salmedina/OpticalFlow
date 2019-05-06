import shlex, subprocess
import os.path as osp
from glob import glob
import argparse
import os

def main(source_path, target_path, sel_method):
    print('Extracting frames from:')
    print(source_path)
    print('Saving flow in:')
    print(target_path)

    source_video_name = 'skip_video.mp4'
    images_prefix = './tmp_gt/i'
    bound = 20

    method = {}
    method['farneback'] = 0
    method['tvl1'] = 1
    method['brox'] = 2
    print('Selected method is {} with value {}'.format(sel_method, method[sel_method]))

    command_path = '/home/zal/Devel/dense_flow/build/extract_gpu'
    all_video_dirs = sorted(glob(osp.join(source_path, '*/')))
    total_videos = len(all_video_dirs)

    for idx, video_dir in enumerate(all_video_dirs):

        video_name = osp.basename(osp.normpath(video_dir))
        video_path = osp.join(video_dir, source_video_name)
        flow_x_prefix = osp.join(target_path, video_name, 'flow_x')
        flow_y_prefix = osp.join(target_path, video_name, 'flow_y')

        os.makedirs(osp.join(target_path, video_name), exist_ok=True)

        command_str = '{} -f={} -x={} -y={} -i={} -b={} -t={} -d=0 -s=1 -o=dir'.format(
            command_path, video_path, flow_x_prefix, flow_y_prefix, images_prefix, bound, method[sel_method])

        args = shlex.split(command_str)
        print('[{}/{}]Extracting flow from {}'.format(idx+1, total_videos, video_name))
        process_result = subprocess.run(args)
        if process_result.returncode != 0:
            print('Failed')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source_dir', help='Dir with all source video dirs')
    parser.add_argument('target_dir', help='Target dir to save optical flow output')
    parser.add_argument('-m', dest='method', default='farneback', help='Options: farneback, tvl1, brox')
    parser.set_defaults(merge=False, visual_debug=False)
    args = parser.parse_args()

    # args.source_dir = '/mnt/Alfheim/Data/DIVA_Proposals/trajectory_images/gt/'
    # args.target_dir = '/mnt/Alfheim/Data/DIVA_Proposals/optical_flow/brox/'
    # args.method = 'brox'

    main(args.source_dir, args.target_dir, args.method)
