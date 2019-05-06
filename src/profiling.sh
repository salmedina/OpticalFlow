#!/usr/bin/zsh

video_dir="/mnt/Alfheim/Data/DIVA_Proposals/OF_Profiling/videos"
frames_dir="/mnt/Alfheim/Data/DIVA_Proposals/trajectory_images/heu_neg_traj_props"
output_dir="/mnt/Alfheim/Data/DIVA_Proposals/OF_Profiling/brox"

rm -rf ${output_dir}/*

for video_path in ${video_dir}/*.mp4; do
    video_name=${video_path:t:r}
    video_frames_dir=${frames_dir}/${video_name}
    video_output_dir=${output_dir}/${video_name}
    mkdir ${video_output_dir}
    /home/zal/Devel/dense_flow/build/extract_gpu -f=${video_frames_dir}/skip_video.mp4 -x=${video_output_dir}/flow_x -y=${video_output_dir}/flow_y -b=20 -t=2 -d=0 -s=1 -o=dir
done