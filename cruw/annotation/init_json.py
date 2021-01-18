import os
import json
import pickle

FOLDER_NAME_DICT = dict(
    cam_0='IMAGES_0',
    cam_1='IMAGES_1',
    rad_h='RADAR_RA_H'
)


def init_anno_json(seq_name, n_frames, dataset='CRUW', fps=30, sensors=None, view=None, setup=None):
    json_dict = dict(
        dataset=dataset,
        date_collect=seq_name[:10],
        seq_name=seq_name,
        n_frames=n_frames,
        fps=fps,
        sensors=sensors,
        view=view,
        setup=setup,
        metadata=init_meta_json(n_frames)
    )
    return json_dict


def init_meta_json(n_frames, folder_name_dict=FOLDER_NAME_DICT,
                   imwidth=1440, imheight=864,
                   rarange=128, raazimuth=128, n_chirps=255):
    meta_all = []
    for frame_id in range(n_frames):
        meta_dict = dict(frame_id=frame_id)
        for key in folder_name_dict.keys():
            if key.startswith('cam'):
                meta_dict[key] = init_camera_json(folder_name_dict[key], imwidth, imheight)
            elif key.startswith('rad'):
                meta_dict[key] = init_radar_json(folder_name_dict[key], rarange, raazimuth, n_chirps)
            else:
                raise NotImplementedError
        meta_all.append(meta_dict)
    return meta_all


def init_camera_json(folder_name, width, height):
    return dict(
        folder_name=folder_name,
        frame_name=None,
        width=width,
        height=height,
        n_objects=0,
        obj_info=dict(
            anno_source=None,
            categories=[],
            bboxes=[],
            scores=[],
            masks=[]
        )
    )


def init_radar_json(folder_name, range, azimuth, n_chirps):
    return dict(
        folder_name=folder_name,
        frame_name=None,
        range=range,
        azimuth=azimuth,
        n_chirps=n_chirps,
        n_objects=0,
        obj_info=dict(
            anno_source=None,
            categories=[],
            centers=[],
            center_ids=[],
            scores=[]
        )
    )
