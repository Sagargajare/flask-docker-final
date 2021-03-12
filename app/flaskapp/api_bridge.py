"""
Created on 03/01/2021

file:           api_bridge.py
description:

@author: Almoutaz
"""

from ctypes import *

hllDll = cdll.LoadLibrary("./libs/libMRZScan.so")
dicG = "./models/mMQDF_f_Passport_bottom_Gray.dic"
dic = "./models/mMQDF_f_Passport_bottom.dic"

func_init_engine = hllDll.InitEngine
func_init_engine.argtypes = [c_char_p, c_char_p]
func_init_engine.restype = c_void_p
engine = func_init_engine(dicG.encode("ascii"), dic.encode("ascii"))

func_scan_mrz = hllDll.ScanMRZ
func_scan_mrz.argtypes = [c_char_p, c_int, c_int]
func_scan_mrz.restype = c_char_p

func_scan_mrz_by_detail = hllDll.ScanMRZByDetail
func_scan_mrz_by_detail.argtypes = [c_char_p, c_int, c_int]
func_scan_mrz_by_detail.restype = c_char_p

def scan_mrz(img, width, height):
    """
    scan mrz from card image

    :param img: opencv mat image
    :param width: width of image
    :param height: height of image
    :return: mrz string
    """
    imgBuffer = img.ctypes.data_as(c_char_p)
    ret = func_scan_mrz(imgBuffer, c_int(width), c_int(height))
    return ret

def scan_mrz_by_detail(img, width, height):
    """
    scan mrz from card image in detail

    :param img: opencv mat image
    :param width: width of image
    :param height: height of image
    :return: mrz string
    """
    imgBuffer = img.ctypes.data_as(c_char_p)
    ret = func_scan_mrz_by_detail(imgBuffer, c_int(width), c_int(height))
    return ret

