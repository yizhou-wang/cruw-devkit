import os
import numpy as np

from .load_txt import read_gt_txt, read_sub_txt, read_rodnet_res
from .rod_eval_utils import compute_ols_dts_gts, evaluate_img, accumulate, summarize

olsThrs = np.around(np.linspace(0.5, 0.9, int(np.round((0.9 - 0.5) / 0.05) + 1), endpoint=True), decimals=2)
recThrs = np.around(np.linspace(0.0, 1.0, int(np.round((1.0 - 0.0) / 0.01) + 1), endpoint=True), decimals=2)


def evaluate_rodnet_seq(res_path, gt_path, n_frame, dataset):

    gt_dets = read_gt_txt(gt_path, n_frame, dataset)
    sub_dets = read_rodnet_res(res_path, n_frame, dataset)

    olss_all = {(imgId, catId): compute_ols_dts_gts(gt_dets, sub_dets, imgId, catId, dataset) \
                for imgId in range(n_frame)
                for catId in range(3)}

    evalImgs = [evaluate_img(gt_dets, sub_dets, imgId, catId, olss_all, olsThrs, recThrs, dataset)
                for imgId in range(n_frame)
                for catId in range(3)]

    return evalImgs

