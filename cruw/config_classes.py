import os
import yaml

from cruw.utils.parse_cam_calib import parse_cam_matrices


class SensorConfig:
    """ SensorConfig class that specifies the dataset sensor setups. """

    def __init__(self,
                 dataset: str,
                 camera_cfg: dict,
                 radar_cfg: dict,
                 calib_cfg: dict):
        self.dataset = dataset
        self.camera_cfg = camera_cfg
        self.radar_cfg = radar_cfg
        self.calib_cfg = calib_cfg

    def serialize(self) -> dict:
        return {
            "dataset": self.dataset,
            "camera_cfg": self.camera_cfg,
            "radar_cfg": self.radar_cfg,
            "calib_cfg": self.calib_cfg
        }

    @classmethod
    def initialize(cls, content: dict):
        return cls(
            content["dataset"],
            content["camera_cfg"],
            content["radar_cfg"],
            content["calib_cfg"]
        )

    def load_cam_calib(self, calib_yaml_l, calib_yaml_r=None):
        with open(calib_yaml_l, "r") as stream:
            data = yaml.safe_load(stream)
            K, D, R, P = parse_cam_matrices(data)
            self.calib_cfg['cam_0'] = {}
            self.calib_cfg['cam_0']['camera_matrix'] = K
            self.calib_cfg['cam_0']['distortion_coefficients'] = D
            self.calib_cfg['cam_0']['rectification_matrix'] = R
            self.calib_cfg['cam_0']['projection_matrix'] = P
        if calib_yaml_r is not None:
            with open(calib_yaml_r, "r") as stream:
                data = yaml.safe_load(stream)
                K, D, R, P = parse_cam_matrices(data)
                self.calib_cfg['cam_1'] = {}
                self.calib_cfg['cam_1']['camera_matrix'] = K
                self.calib_cfg['cam_1']['distortion_coefficients'] = D
                self.calib_cfg['cam_1']['rectification_matrix'] = R
                self.calib_cfg['cam_1']['projection_matrix'] = P

    def load_cam_calibs(self, data_root, calib_yaml_paths):
        self.calib_cfg['cam_calib'] = {}
        self.calib_cfg['cam_calib']['load_success'] = True
        for date in calib_yaml_paths.keys():
            self.calib_cfg['cam_calib'][date] = {}
            n_paths = len(calib_yaml_paths[date])
            calib_yaml_path = os.path.join(data_root, calib_yaml_paths[date][0])
            if os.path.exists(calib_yaml_path):
                with open(calib_yaml_path, "r") as stream:
                    data = yaml.safe_load(stream)
                    K, D, R, P = parse_cam_matrices(data)
                    self.calib_cfg['cam_calib'][date]['cam_0'] = {}
                    self.calib_cfg['cam_calib'][date]['cam_0']['camera_matrix'] = K
                    self.calib_cfg['cam_calib'][date]['cam_0']['distortion_coefficients'] = D
                    self.calib_cfg['cam_calib'][date]['cam_0']['rectification_matrix'] = R
                    self.calib_cfg['cam_calib'][date]['cam_0']['projection_matrix'] = P
            else:
                self.calib_cfg['cam_calib']['load_success'] = False
            if n_paths == 2:
                calib_yaml_path = os.path.join(data_root, calib_yaml_paths[date][1])
                if os.path.exists(calib_yaml_path):
                    with open(calib_yaml_path, "r") as stream:
                        data = yaml.safe_load(stream)
                        K, D, R, P = parse_cam_matrices(data)
                        self.calib_cfg['cam_calib'][date]['cam_1'] = {}
                        self.calib_cfg['cam_calib'][date]['cam_1']['camera_matrix'] = K
                        self.calib_cfg['cam_calib'][date]['cam_1']['distortion_coefficients'] = D
                        self.calib_cfg['cam_calib'][date]['cam_1']['rectification_matrix'] = R
                        self.calib_cfg['cam_calib'][date]['cam_1']['projection_matrix'] = P
                else:
                    self.calib_cfg['cam_calib']['load_success'] = False


class ObjectConfig:
    """ ObjectConfig class that specifies the object configurations in the dataset. """

    def __init__(self,
                 n_class: int,
                 classes: list,
                 sizes: dict):
        self.n_class = n_class
        self.classes = classes
        self.sizes = sizes

    def serialize(self) -> dict:
        return {
            "n_classes": self.n_class,
            "classes": self.classes,
            "sizes": self.sizes
        }

    @classmethod
    def initialize(cls, content: dict):
        return cls(
            content["n_classes"],
            content["classes"],
            content["sizes"]
        )


class HumanAnnoConfig:
    def __init__(self,
                 gt_root: str,
                 gt_dir_name: str,
                 gt_format: str,
                 seq_names: list,
                 dataset: str,
                 date_included: bool,
                 output_dir: str):
        self.gt_root = gt_root
        self.gt_dir_name = gt_dir_name
        self.gt_format = gt_format
        self.seq_names = seq_names
        self.dataset = dataset
        self.date_included = date_included
        self.output_dir = output_dir

    def serialize(self) -> dict:
        return {
            "gt_root": self.gt_root,
            "gt_dir_name": self.gt_dir_name,
            "gt_format": self.gt_format,
            "seq_names": self.seq_names,
            "dataset": self.dataset,
            "date_included": self.date_included,
            "output_dir": self.output_dir
        }

    @classmethod
    def initialize(cls, content: dict):
        return cls(
            content['gt_root'],
            content['gt_dir_name'],
            content['gt_format'],
            content['seq_names'],
            content['dataset'],
            content['date_included'],
            content['output_dir']
        )


class Loc3DCamConfig:
    """ Data class that specifies the camera 3D localization evaluation settings. """

    def __init__(self,
                 seq_names: list,
                 res_root: str,
                 res_dir_name: str,
                 res_format: str,
                 min_dist_thres: float,
                 gt_root: str = None,
                 gt_dir_name: str = None,
                 gt_format: str = None,
                 date_included: bool = True):
        self.seq_names = seq_names
        self.res_root = res_root
        self.res_dir_name = res_dir_name
        self.res_format = res_format
        self.min_dist_thres = min_dist_thres
        self.gt_root = gt_root
        self.gt_dir_name = gt_dir_name
        self.gt_format = gt_format
        self.date_included = date_included

    def serialize(self) -> dict:
        if self.gt_root is not None:
            return {
                "seq_names": self.seq_names,
                "res_root": self.res_root,
                "res_dir_name": self.res_dir_name,
                "res_format": self.res_format,
                "min_dist_thres": self.min_dist_thres,
                "gt_root": self.gt_root,
                "gt_dir_name": self.gt_dir_name,
                "gt_format": self.gt_format,
                "date_included": self.date_included
            }
        else:
            return {
                "seq_names": self.seq_names,
                "res_root": self.res_root,
                "res_dir_name": self.res_dir_name,
                "res_format": self.res_format,
                "min_dist_thres": self.min_dist_thres,
                "date_included": self.date_included
            }

    @classmethod
    def initialize(cls, content: dict):
        if 'gt_root' in content:
            return cls(
                content['seq_names'],
                content['res_root'],
                content['res_dir_name'],
                content['res_format'],
                content['min_dist_thres'],
                content['gt_root'],
                content['gt_dir_name'],
                content['gt_format'],
                content['date_included']
            )
        else:
            return cls(
                content['seq_names'],
                content['res_root'],
                content['res_dir_name'],
                content['res_format'],
                content['min_dist_thres'],
                content['date_included']
            )
