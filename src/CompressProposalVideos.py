import shlex, subprocess
import os.path as osp
from glob import glob
import os

def main():
    gt_videos_dir= '/mnt/Alfheim/Data/DIVA_Proposals/trajectory_images/gt/'
    heu_videos_dir = '/mnt/Alfheim/Data/DIVA_Proposals/trajectory_images/heu_neg_traj_props/'


    videos_path = heu_videos_dir

    all_video_dirs = sorted(glob(osp.join(videos_path, '*/')))
    total_videos = len(all_video_dirs)

    for idx, video_dir in enumerate(all_video_dirs):
        video_name = osp.basename(osp.normpath(video_dir))
        output_path = osp.join(video_dir, 'skip_video.mp4')
        frames_template_str = osp.join(video_dir, '%s-%%06d.jpg' % video_name)

        command_str = 'ffmpeg -y -hide_banner -loglevel panic -i {} -c:v libx264 -pix_fmt yuv420p {}'.format(
            frames_template_str, output_path)

        args = shlex.split(command_str)
        print('[{}/{}] Compressing video {}'.format(idx+1, total_videos, video_name))
        process_result = subprocess.run(args)
        if process_result.returncode != 0:
            print('Failed')
            print(process_result.stdout, process_result.stderr)


if __name__ == '__main__':
    main()