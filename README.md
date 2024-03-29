# CRUW devkit

Package `cruw-devkit` is a useful toolkit for the CRUW dataset including sensor configurations, sensor calibration parameters, 
the mapping functions, metadata, visualization tools, etc. More components are still in the developing phase. 

Please refer to our [dataset website](https://www.cruwdataset.org) for more information about the CRUW Dataset.

This repository is maintained by [Yizhou Wang](http://yizhouwang.net/). Free to raise issues and help improve this 
repository.

## Acknowledgment for CRUW dataset

**ACADEMIC OR NON-PROFIT ORGANIZATION NONCOMMERCIAL RESEARCH USE ONLY**

This research is mainly conducted by the [Information Processing Lab (IPL)](https://ipl-uw.github.io/) at the 
University of Washington. It was partially supported by CMMB Vision – UWECE Center on Satellite Multimedia and 
Connected Vehicles. We would also like to thank the colleagues and students in IPL for their help and assistance on the 
dataset collection, processing, and annotation works.

## News
- [2022/01/01] ROD2021 evaluation server is reopened. Welcome to submit your results! [[Evaluation Server]](https://codalab.lisn.upsaclay.fr/competitions/1063)
- [2021/11/17] ROD2021 Challenge Session @ ACM ICMR 2021. [[Challenge Summary Paper]](https://dl.acm.org/doi/abs/10.1145/3460426.3463658)
- [2021/06/20] Our work is presented in the Workshop on Autonomous Driving (WAD) at CVPR 2021. 
  Code will be release soon. 
  [[Paper]](https://openaccess.thecvf.com/content/CVPR2021W/WAD/html/Wang_Rethinking_of_Radars_Role_A_Camera-Radar_Dataset_and_Systematic_Annotator_CVPRW_2021_paper.html)
  [[Spotlight]](https://youtu.be/gLu-lVM3X7s)
  [[Poster]](http://yizhouwang.net/documents/wad_cvpr2021_poster.pdf)
  [[WAD Full Video]](https://youtu.be/eOL_rCK59ZI)
- [2021/02/06] The journal version of the RODNet paper is accepted by IEEE J-STSP. 
  [[Paper]](https://ieeexplore.ieee.org/document/9353210)
  [[ArXiv]](https://arxiv.org/abs/2102.05150)
  [[Code]](https://github.com/yizhou-wang/RODNet)
  [[Demo]](https://youtu.be/09HaDySa29I)
- [2020/12/20] We are organizing the [ROD2021 Challenge](https://www.cruwdataset.org/rod2021) at ACM ICMR 2021. Welcome your participation!
- [2020/11/01] Our radar object detection paper (RODNet) is accepted by  WACV 2021. 
  [[Paper]](https://openaccess.thecvf.com/content/WACV2021/html/Wang_RODNet_Radar_Object_Detection_Using_Cross-Modal_Supervision_WACV_2021_paper.html)
  [[Code]](https://github.com/yizhou-wang/RODNet)
  [[Presentation]](https://youtu.be/UZbxI4o2-7g)
  
## Changelog

- [2022/02/02] add dataset script and fix installation bugs
- [2022/01/28] v1.1: add coordinate transform and other utils.
- [2022/01/27] handle camera images unavailable issue for ROD2021 testing set.
- [2022/01/25] add functions to transfer RF images/labels from polar to Cartesian coordinates.
- [2021/12/03] add evaluation for RODNet format results.
- [2021/11/09] add sensor config files.
- [2021/11/01] add some utils functions for evaluation.
- [2021/01/18] v1.0: stable version for ROD2021 Challenge.

## Installation

Create a new conda environment. Tested under Python 3.6, 3.7, 3.8.
```
conda create -n cruw-devkit python=3.*
```
Run setup tool for this devkit.
```
conda activate cruw-devkit
pip install .
pip install -e .  # development mode
```

## Tutorials

The tutorials for the usages of `cruw-devkit` package are listed in the tutorial folder.
- For ROD2021 Challenge: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yizhou-wang/cruw-devkit/blob/master/tutorials/cruw_devkit_tutorial_rod2021.ipynb)


## Annotation Format

### ROD2021 Dataset

Each training sequence (40 training sequences in total) has an `txt` object annotation file. 
The annotation format for the training set (each line in the `txt` files):
```
  frame_id range(m) azimuth(rad) class_name
  ...
```

### General CRUW Dataset

For each sequence, a `json` file is provided as annotations:
```
{
  "dataset": "CRUW",
  "date_collect": "2019_09_29",
  "seq_name": "2019_09_29_onrd000",
  "n_frames": 1694,
  "fps": 30,
  "sensors": "C2R2",                  // <str>: "C1R1", "C2R1", "C2R2"
  "view": "front",                    // <str>: "front", "right-side"
  "setup": "vehicle",                 // <str>: "cart", "vehicle"
  "metadata": [
    {  // metadata for each frame
      "frame_id": 0,
      "cam_0": {
        "folder_name": "images_0",
        "frame_name": "0000000000.jpg",
        "width": 1440,
        "height": 864,
        "n_objects": 5,
        "obj_info": {
          "anno_source": "human",     // <str>: "human", "mrcnn", etc.
          "categories": [],           // <str> [n_objects]: category names
          "bboxes": [],               // <int> [n_objects, 4]: xywh
          "scores": [],               // <float> [n_objects]: confidence scores [0, 1]
          "masks": [],                // <rle_code> [n_objects]: instance masks
          "visibilities": [],         // <float> [n_objects]: [0, 1]
          "truncations": [],          // <float> [n_objects]: [0, 1]
          "translations": []          // <float> [n_objects, 3]: xyz(m)
        }
      },
      "cam_1": {
        "folder_name": "images_1",
        "frame_name": "0000000000.jpg",
        "width": 1440,
        "height": 864,
        "n_objects": 5,
        "obj_info": {
          "anno_source": "human",     // <str>: "human", "mrcnn", etc.
          "categories": [],           // <str> [n_objects]: category names
          "bboxes": [],               // <int> [n_objects, 4]: xywh
          "scores": [],               // <float> [n_objects]: confidence scores [0, 1]
          "masks": [],                // <rle_code> [n_objects]: instance masks
          "visibilities": [],         // <float> [n_objects]: [0, 1]
          "truncations": [],          // <float> [n_objects]: [0, 1]
          "translations": []          // <float> [n_objects, 3]: xyz(m)
        }
      },
      "radar_h": {
        "folder_name": "radar_chirps_win_RISEP_h",
        "frame_name": "000000.npy",
        "range": 128,
        "azimuth": 128,
        "n_chirps": 255,
        "n_objects": 3,
        "obj_info": {
          "anno_source": "human",     // <str>: "human", "co", "crf", etc.
          "categories": [],           // <str> [n_objects]: category names
          "centers": [],              // <float> [n_objects, 2]: range(m), azimuth(rad)
          "center_ids": [],           // <int> [n_objects, 2]: range indices, azimuth indices
          "scores": []                // <float> [n_objects]: confidence scores [0, 1]
        }
      },
      "radar_v": {
        "folder_name": "radar_chirps_win_RISEP_v",
        "frame_name": "000000.npy",
        "range": 128,
        "azimuth": 128,
        "n_chirps": 255,
        "n_objects": 3,
        "obj_info": {
          "anno_source": "human",     // <str>: "human", "co", "crf", etc.
          "categories": [],           // <str> [n_objects]: category names
          "centers": [],              // <float> [n_objects, 2]: range(m), azimuth(rad)
          "center_ids": [],           // <int> [n_objects, 2]: range indices, azimuth indices
          "scores": []                // <float> [n_objects]: confidence scores [0, 1]
        }
      }
    },
    {...}
  ]
}
```
