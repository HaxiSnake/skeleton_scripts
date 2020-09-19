import os
import cv2

video_src_dir = "/skating2.0/extracted_videos"
video_dst_dir = "/skating2.0/removed_empty_frame_videos"

if os.path.exists(video_dst_dir):
    os.system("rm -rf "+video_dst_dir)
os.makedirs(video_dst_dir)

count = 0
for video_name in os.listdir(video_src_dir):
    count += 1
    print(video_name)
    if video_name.split(".")[-1] == "mp4":
        video_path = os.path.join(video_src_dir, video_name)
        camera = cv2.VideoCapture(video_path)
        fps = camera.get(5)
        fps = int(fps) 
        width = camera.get(3)
        height = camera.get(4)
        print("video frame: ", camera.get(7))
        size = (int(width), int(height))

        video_out_path = os.path.join(video_dst_dir, video_name)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(video_out_path, fourcc, 30, size)
        print(video_out_path)
        ret, img = camera.read()
        frame_count = 0
        while ret:
            # if img.empty():
            #     print("empty frame:", frame_count)
            frame_count += 1
            writer.write(img)
            ret, img = camera.read()
            
        print("video real frame: ", frame_count)
        camera.release()
        writer.release()
