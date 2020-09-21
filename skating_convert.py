import os
import sys
import argparse
import json
import shutil

import video
from utils import *


def pose_estimation(openpose, out_folder, video_path, model_name, model_folder, info, p):
    video_name = video_path.split('/')[-1].split('.')[0]
    output_snippets_dir = os.path.join(out_folder,'openpose_estimation/{}/{}'.format(model_name, video_name))
    output_sequence_dir = os.path.join(out_folder,'{}_data/'.format(p))
    if not os.path.exists(output_sequence_dir):
        os.makedirs(output_sequence_dir)
    output_sequence_path = '{}/{}.json'.format(output_sequence_dir, video_name)
    # pose estimation
    openpose_args = dict(
        video=video_path,
        write_json=output_snippets_dir,
        display=0,
        render_pose=0, 
        model_pose=model_name,
        model_folder=model_folder)
    command_line = openpose + ' '
    command_line += ' '.join(['--{} {}'.format(k, v) for k, v in openpose_args.items()])
    shutil.rmtree(output_snippets_dir, ignore_errors=True)
    os.makedirs(output_snippets_dir)
    LOGGER.info(command_line)
    os.system(command_line)
    # pack openpose ouputs
    video_obj = video.get_video_frames(video_path)
    height, width, _ = video_obj[0].shape
    video_info = json_pack(
        output_snippets_dir, video_name, width, height, label_index=info["label_index"],label=info["label"])
    if not os.path.exists(output_sequence_dir):
        os.makedirs(output_sequence_dir)
    with open(output_sequence_path, 'w') as outfile:
        json.dump(video_info, outfile)
    if len(video_info['data']) == 0:
        LOGGER.info('Can not find pose estimation results of %s'%(video_name))
        return
    else:
        LOGGER.info('%s Pose estimation complete.'%(video_name))    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Skating Data Converter.')
    # region arguments yapf: disable
    parser.add_argument('--openpose',
        default='/openpose/build',
        help='Path to openpose')
    parser.add_argument(
        '--data_path', default='/skating2.0/skating63',help="Path to dataset")
    parser.add_argument(
        '--out_folder', default='/skating2.0/skating63_openpose_result',help="Path to save files")
    parser.add_argument(
        '--model_folder', default='/openpose/models',help="Path to model folder")
    arg = parser.parse_args()
    arg.trainfile=os.path.join(arg.data_path,"label_train_skating63.csv")
    arg.testfile=os.path.join(arg.data_path,"label_val_skating63.csv")
    openpose='{}/examples/openpose/openpose.bin'.format(arg.openpose)
    LOGGER.info(os.getcwd())
    part = ['label_train_skating63', 'label_val_skating63']
    restart_list = {
        'label_train_skating63': 3566,
        'label_val_skating63': 0
    }
    debug = False
    debug_count = 2
    for p in part:
        csvfile=os.path.join(arg.data_path,"{}.csv".format(p))
        total_count = count_lines(csvfile)
        count = 0
        restart_count = restart_list[p]
        for category, video_name, label in name_loader(csvfile):
            if debug and count >= debug_count:
                break
            if count < restart_count:
                count += 1
                continue
            # try:
            video_name = video_name + ".mp4"
            info={}
            info['label_index']=int(label)
            info['has_skeleton']=True
            info['label']=category
            video_path = os.path.join(arg.data_path, category, video_name)
            if not os.path.exists(video_path):
                LOGGER.info("%s not exist"%(video_path))
            count+=1
            msg = '{}:({:>5}/{:<5}) Processing data: '.format(p,  count, total_count)
            print_toolbar(count * 100.0 / total_count, msg)
            pose_estimation(openpose, arg.out_folder,video_path, "BODY_25",arg.model_folder,info,p)
            # except Exception as e:
            #     LOGGER.warning(e)
