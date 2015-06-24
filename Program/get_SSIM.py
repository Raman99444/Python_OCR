"""
This module computes the Structured Similarity Image Metric (SSIM)

Created on 23 Jun. 2015

"""



import numpy as np
import scipy.ndimage
from numpy.ma.core import exp, sqrt
from scipy.constants.constants import pi
import numexpr as ne
import cv2

def _to_grayscale(bgr_image):
    int_image = bgr_image.astype('uint32')
    int_image[:,:,2] *= 299
    int_image[:,:,1] *= 587
    int_image[:,:,0] *= 114

    luma = np.sum(int_image, axis = 2) / 1000
    return luma.astype('float')

def create_gaussian_kernel(gaussian_kernel_sigma = 1.5, gaussian_kernel_width = 11):
    # 1D Gaussian kernel definition
    gaussian_kernel = np.ndarray((gaussian_kernel_width))
    mu = int(gaussian_kernel_width / 2)

    #Fill Gaussian kernel
    for i in range(gaussian_kernel_width):
            gaussian_kernel[i] = (1 / (sqrt(2 * pi) * (gaussian_kernel_sigma))) * \
                exp(-(((i - mu) ** 2)) / (2 * (gaussian_kernel_sigma ** 2)))

    return gaussian_kernel

def convolve_gaussian_2d(image, gaussian_kernel_1d):
    result = scipy.ndimage.filters.correlate1d(image, gaussian_kernel_1d, axis = 0)
    result = scipy.ndimage.filters.correlate1d(result, gaussian_kernel_1d, axis = 1)
    return result
	
	
	