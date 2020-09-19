import os
from utils import name_loader
import video
dataset_path = "/skating2.0/skating63/"

with open("frame_err.log","w") as log_file:
    parts =  ['label_train_skating63', 'label_val_skating63']
    for part in parts:
        csvfile = os.path.join(dataset_path, "{}.csv".format(part))
        for category, video_name, label in name_loader(csvfile):
            video_path = os.path.join(dataset_path, category, video_name + ".mp4")
            try:
                print("read video: {}".format(video_path))
                video_obj = video.get_video_frames(video_path)
            except RuntimeError as e:
                print("{} Runtime Error: {}".format(video_path, str(e)))
                msg = video_name + " ### " + str(e) + "\n"
                log_file.write(msg)
