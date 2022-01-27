import os
import numpy as np

from .load_txt import read_gt_txt, read_sub_txt
from .rod_eval_utils import compute_ols_dts_gts, evaluate_img, accumulate, summarize

olsThrs = np.around(np.linspace(0.5, 0.9, int(np.round((0.9 - 0.5) / 0.05) + 1), endpoint=True), decimals=2)
recThrs = np.around(np.linspace(0.0, 1.0, int(np.round((1.0 - 0.0) / 0.01) + 1), endpoint=True), decimals=2)


def evaluate_rod2021(submit_dir, truth_dir, dataset):
    sub_names = sorted(os.listdir(submit_dir))
    gt_names = sorted(os.listdir(truth_dir))
    assert len(sub_names) == len(gt_names), "missing submission files!"
    for sub_name, gt_name in zip(sub_names, gt_names):
        if sub_name != gt_name:
            raise AssertionError("wrong submission file names!")

    # evaluation start
    evalImgs_all = []
    n_frames_all = 0

    for seqid, (sub_name, gt_name) in enumerate(zip(sub_names, gt_names)):
        gt_path = os.path.join(truth_dir, gt_name)
        sub_path = os.path.join(submit_dir, sub_name)
        data_path = os.path.join(dataset.data_root, 'sequences', 'test', gt_names[seqid][:-4])
        # n_frame = len(os.listdir(os.path.join(data_path, dataset.sensor_cfg.camera_cfg['image_folder'])))
        n_frame = int(len(os.listdir(os.path.join(data_path, dataset.sensor_cfg.radar_cfg['chirp_folder']))) / len(
            dataset.sensor_cfg.radar_cfg['chirp_ids']))

        gt_dets = read_gt_txt(gt_path, n_frame, dataset)
        sub_dets = read_sub_txt(sub_path, n_frame, dataset)

        olss_all = {(imgId, catId): compute_ols_dts_gts(gt_dets, sub_dets, imgId, catId, dataset) \
                    for imgId in range(n_frame)
                    for catId in range(3)}

        evalImgs = [evaluate_img(gt_dets, sub_dets, imgId, catId, olss_all, olsThrs, recThrs, dataset)
                    for imgId in range(n_frame)
                    for catId in range(3)]

        n_frames_all += n_frame
        evalImgs_all.extend(evalImgs)

    eval = accumulate(evalImgs_all, n_frames_all, olsThrs, recThrs, dataset, log=False)
    stats = summarize(eval, olsThrs, recThrs, dataset, gl=False)
    print("AP_total: %.4f" % (stats[0] * 100))
    print("AR_total: %.4f" % (stats[1] * 100))
