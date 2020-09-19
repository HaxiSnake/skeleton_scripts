import os
import sys

video_src_dir = "/share/skating2.0/removed_empty_frame_videos"
video_dst_dir = "/share_4t/skating63"

record_file = "/share/skating2.0/skeleton_script/frame_err.log"

# if not os.path.exists(video_dst_dir):
#     os.makedirs(video_dst_dir)
# else:
#     os.system("rm -r " + video_dst_dir)
#     os.makedirs(video_dst_dir)

with open(record_file, 'r') as f:
    for line in f.readlines():
        video_name = line.strip().split(" ")[0]
        class_name = video_name.split("_n")[0]
        # src_dir/class_name/video_name.mp4
        video_src_path = os.path.join(video_src_dir, video_name + ".mp4")
        video_dst_path = os.path.join(video_dst_dir, class_name, video_name + ".mp4")
        command = "cp " + video_src_path + " " + video_dst_path
        sys.stdout.write(command+"\n")
        os.system(command)