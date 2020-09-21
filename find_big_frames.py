import os

def name_loader(filename):
    with open(filename) as f:
        for line in f.readlines():
            info=line.strip()
            category, video_name, frame_num, label = info.split(",")
            yield category, video_name, frame_num, label

dataset_path = "/skating2.0/skating63/"

parts =  ['label_train_skating63', 'label_val_skating63']
for part in parts:
    csvfile = os.path.join(dataset_path, "{}.csv".format(part))
    for category, video_name, frame_num, label in name_loader(csvfile):
        video_path = os.path.join(dataset_path, category, video_name + ".mp4")
        if int(frame_num) > 2000:
            print("big frame:", video_name, frame_num)