import logging
from pathlib import Path
import json

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(level = logging.INFO)
handler = logging.FileHandler("convert.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

toolbar_width = 30

def print_toolbar(rate, annotation=''):
    # setup toolbar
    LOGGER.info("{}[".format(annotation))
    # for i in range(toolbar_width):
    #     if i * 1.0 / toolbar_width > rate:
    #         LOGGER.info(' ')
    #     else:
    #         LOGGER.info('-')
    # LOGGER.info(']\r')


def end_toolbar():
    LOGGER.info("\n")

def count_lines(filename):
    with open(filename) as f:
        count=-1
        for count,_ in enumerate(f):
            pass
        count+=1
    return count


def name_loader(filename):
    with open(filename) as f:
        for line in f.readlines():
            info=line.strip()
            category, video_name, frame_num, label = info.split(",")
            yield category, video_name, label
        

def json_pack(snippets_dir, video_name, frame_width, frame_height, label='unknown', label_index=-1):
    sequence_info = []
    p = Path(snippets_dir)
    for path in p.glob(video_name+'*.json'):
        json_path = str(path)
        # LOGGER.info(path)
        frame_id = int(path.stem.split('_')[-2])
        frame_data = {'frame_index': frame_id}
        data = json.load(open(json_path))
        skeletons = []
        for person in data['people']:
            score, coordinates = [], []
            skeleton = {}
            keypoints = person['pose_keypoints_2d']
            for i in range(0, len(keypoints), 3):
                coordinates += [keypoints[i]/frame_width, keypoints[i + 1]/frame_height]
                score += [keypoints[i + 2]]
            skeleton['pose'] = coordinates
            skeleton['score'] = score
            skeletons += [skeleton]
        frame_data['skeleton'] = skeletons
        sequence_info += [frame_data]

    video_info = dict()
    video_info['data'] = sequence_info
    video_info['label'] = label
    video_info['label_index'] = label_index

    return video_info