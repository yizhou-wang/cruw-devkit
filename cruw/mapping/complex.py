import numpy as np


def ri2ap(mat_ri):
    mat_ap = np.zeros_like(mat_ri)
    rf_complex = mat_ri[:, :, 0] + mat_ri[:, :, 1] * 1j
    mat_ap[:, :, 0] = np.abs(rf_complex)
    mat_ap[:, :, 1] = np.angle(rf_complex)
    return mat_ap


def ap2ri(mat_ap):
    mat_ri = np.zeros_like(mat_ap)
    rf_complex = mat_ap[:, :, 0] * np.exp(mat_ap[:, :, 1] * 1j)
    mat_ri[:, :, 0] = np.real(rf_complex)
    mat_ri[:, :, 1] = np.imag(rf_complex)
    return mat_ri


if __name__ == '__main__':
    mat_ri = np.random.rand(2, 2, 2)
    mat_ap = ri2ap(mat_ri)
    mat_ri_2 = ap2ri(mat_ap)
    mat_ap_2 = ri2ap(mat_ri_2)
