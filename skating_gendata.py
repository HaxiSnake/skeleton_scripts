import os
import sys
import pickle
import argparse

import numpy as np
from numpy.lib.format import open_memmap

from feeder_skating import Feeder_skating


toolbar_width = 30

def print_toolbar(rate, annotation=''):
    # setup toolbar
    sys.stdout.write("{}[".format(annotation))
    for i in range(toolbar_width):
        if i * 1.0 / toolbar_width > rate:
            sys.stdout.write(' ')
        else:
            sys.stdout.write('-')
        sys.stdout.flush()
    sys.stdout.write(']\r')


def end_toolbar():
    sys.stdout.write("\n")


def gendata(
        data_path,
        label_path,
        data_out_path,
        label_out_path,
        num_person_in=5,  #observe the first 5 persons 
        num_person_out=1,  #then choose 2 persons with the highest score 
        max_frame=2500,
        joins_count=25):

    feeder = Feeder_skating(
        data_path=data_path,
        label_path=label_path,
        num_person_in=num_person_in,
        num_person_out=num_person_out,
        joins_count=joins_count,
        debug=False,
        window_size=max_frame)

    sample_name = feeder.sample_name
    sample_label = []

    fp = open_memmap(
        data_out_path,
        dtype='float32',
        mode='w+',
        shape=(len(sample_name), 3, max_frame, joins_count, num_person_out))

    for i, s in enumerate(sample_name):
        data, label = feeder[i]
        print_toolbar(i * 1.0 / len(sample_name),
                      '({:>5}/{:<5}) Processing data: '.format(
                          i + 1, len(sample_name)))
        fp[i, :, 0:data.shape[1], :, :] = data
        sample_label.append(label)

    with open(label_out_path, 'wb') as f:
        pickle.dump((sample_name, list(sample_label)), f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Skating-skeleton Data Converter.')
    parser.add_argument(
        '--data_path', default='/skating2.0/skating63_openpose_result')
    parser.add_argument(
        '--out_folder', default='/skating2.0/skating63_openpose_result/skeleton_file')
    arg = parser.parse_args()

    part = ['label_train_skating63', 'label_val_skating63']
    for p in part:
        data_path = '{}/{}_data'.format(arg.data_path, p)  
        label_path = '{}/{}.csv'.format(arg.data_path, p)
        data_out_path = '{}/{}_data.npy'.format(arg.out_folder, p)
        label_out_path = '{}/{}_label.pkl'.format(arg.out_folder, p)

        if not os.path.exists(arg.out_folder):
            os.makedirs(arg.out_folder)
        gendata(data_path, label_path, data_out_path, label_out_path)
