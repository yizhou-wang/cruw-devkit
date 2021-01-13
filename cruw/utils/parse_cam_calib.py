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
