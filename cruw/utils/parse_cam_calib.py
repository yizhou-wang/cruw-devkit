import numpy as np


def parse_cam_matrices(data):
    camera_matrix = data['camera_matrix']
    distortion_coefficients = data['distortion_coefficients']
    rectification_matrix = data['rectification_matrix']
    projection_matrix = data['projection_matrix']

    K = np.array(camera_matrix['data'])
    K = np.reshape(K, (camera_matrix['rows'], camera_matrix['cols']))
    D = np.array(distortion_coefficients['data'])
    D = np.reshape(D, (distortion_coefficients['rows'], distortion_coefficients['cols']))
    D = np.squeeze(D)
    R = np.array(rectification_matrix['data'])
    R = np.reshape(R, (rectification_matrix['rows'], rectification_matrix['cols']))
    P = np.array(projection_matrix['data'])
    P = np.reshape(P, (projection_matrix['rows'], projection_matrix['cols']))

    return K, D, R, P


def parse_cam_matrices_cruw2022(data):
    calib_dict = {}
    intrin = data['intrinsic']
    intrin = np.array(intrin)
    intrin = np.reshape(intrin, (3, 4))
    intrin = intrin[:3, :3]
    extrin = data['extrinsic']
    extrin = np.array(extrin)
    extrin = np.reshape(extrin, (4, 4))
    calib_dict['intrinsic'] = intrin
    calib_dict['extrinsic'] = extrin
    return calib_dict
