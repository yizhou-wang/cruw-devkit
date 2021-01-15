import sys

from cruw import CRUW
from cruw.eval import evaluate_rod2021

if __name__ == '__main__':
    data_root = "/mnt/disk1/CRUW/ROD2021"
    dataset = CRUW(data_root=data_root, sensor_config_name='sensor_config_rod2021')
    submit_dir = sys.argv[1]
    truth_dir = sys.argv[2]
    evaluate_rod2021(submit_dir, truth_dir, dataset)
