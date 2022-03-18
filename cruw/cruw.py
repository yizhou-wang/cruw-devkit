import os
import json

from cruw.config_classes import SensorConfig, ObjectConfig
from cruw.mapping import confmap2ra, labelmap2ra, get_xzgrid


class CRUW:
    """ Dataset class for CRUW. """

    def __init__(self,
                 data_root: str,
                 sensor_config_name: str = 'sensor_config',
                 object_config_name: str = 'object_config'):
        self.data_root = data_root
        self.sensor_cfg = self._load_sensor_config(sensor_config_name)
        self.dataset = self.sensor_cfg.dataset
        self.object_cfg = self._load_object_config(object_config_name)

        self.range_grid = confmap2ra(self.sensor_cfg.radar_cfg, name='range')
        self.angle_grid = confmap2ra(self.sensor_cfg.radar_cfg, name='angle')
        try:
            self.range_grid_label = labelmap2ra(self.sensor_cfg.radar_cfg, name='range')
            self.angle_grid_label = labelmap2ra(self.sensor_cfg.radar_cfg, name='angle')
        except:
            self.range_grid_label = None
            self.angle_grid_label = None
            print('not using range_grid_label and angle_grid_label.')

        self.xz_grid = get_xzgrid(self.sensor_cfg.radar_cfg['xz_dim'], self.sensor_cfg.radar_cfg['z_max'])

    def __str__(self):
        print_log = '<CRUW Dataset Object>\n'
        print_log += "Dataset name:   %s\n" % self.dataset
        cam_flag = True if self.sensor_cfg.camera_cfg else False
        rad_flag = True if self.sensor_cfg.radar_cfg else False
        print_log += "Sensor configs: camera = %s | radar = %s\n" % (str(cam_flag).ljust(5), str(rad_flag).ljust(5))
        cam_calib_flag = True if self.sensor_cfg.calib_cfg['cam_calib_paths'] else False
        print_log += "Calibration:    camera = %s | cross = %s\n" % (str(cam_calib_flag).ljust(5), str(True).ljust(5))
        print_log += "Object configs: n_class = %d\n" % self.object_cfg.n_class
        mapping_flag = True if len(self.angle_grid) != 0 and len(self.range_grid) != 0 else False
        print_log += "Coor mappings:  %s\n" % mapping_flag
        return print_log

    def _load_sensor_config(self, config_name) -> SensorConfig:
        """
        Create a SensorConfig class for CRUW dataset.
        The config file is located in 'cruw/dataset_configs' folder.
        :param config_name: Name of configuration
        :return: SensorConfig
        """
        # check if config exists
        this_dir = os.path.dirname(os.path.abspath(__file__))
        cfg_path = os.path.join(this_dir, 'dataset_configs', '%s.json' % config_name)
        if os.path.exists(cfg_path):
            # load config file from dataset_configs folder
            with open(cfg_path, 'r') as f:
                data = json.load(f)
        elif os.path.exists(config_name):
            # load config file from an outside json file
            with open(config_name, 'r') as f:
                data = json.load(f)
        else:
            assert os.path.exists(cfg_path), 'Configuration {} not found'.format(config_name)

        cfg = SensorConfig.initialize(data)
        # cam_0_calib_yaml = os.path.join(self.data_root, 'calib', cfg.calib_cfg['cam_calib_name'], 'left.yaml')
        # cam_1_calib_yaml = os.path.join(self.data_root, 'calib', cfg.calib_cfg['cam_calib_name'], 'right.yaml')
        # cfg.load_cam_calib(cam_0_calib_yaml, cam_1_calib_yaml)
        cfg.load_cam_calibs(self.data_root, cfg.calib_cfg['cam_calib_paths'])
        if not cfg.calib_cfg['cam_calib']['load_success']:
            print('warning: loading calibration data failed')

        return cfg

    def _load_object_config(self, config_name) -> ObjectConfig:
        """
        Create a ObjectConfig class for CRUW dataset.
        The config file is located in 'cruw/dataset_configs' folder.
        :param config_name: Name of configuration
        :return: ObjectConfig
        """
        # check if config exists
        this_dir = os.path.dirname(os.path.abspath(__file__))
        cfg_path = os.path.join(this_dir, 'dataset_configs', '%s.json' % config_name)
        assert os.path.exists(cfg_path), 'Configuration {} not found'.format(config_name)

        # load config file to Loc3DCamConfig
        with open(cfg_path, 'r') as f:
            data = json.load(f)
        cfg = ObjectConfig.initialize(data)

        return cfg
