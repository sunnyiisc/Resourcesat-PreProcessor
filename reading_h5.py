"""
Created on 27 Mar, 2024 at 11:10
    Title: reading_h5.py - ...
    Description:
        -   ...
@author: Supantha Sen, nrsc, ISRO
"""

# Importing Modules
import h5py
import pathlib
import numpy as np
import cv2

# Importing Custom Modules
...

...


def read_h5_angles(prod_path):
    data_h5 = h5py.File(prod_path, 'r')

    ##Extracting the Angle Bands
    scan_pix = []
    sun_azi_ang, sun_ele_ang, sat_azi_ang, sat_ele_ang = [], [], [], []
    for data in data_h5['Geo_Location']['Navigation_Info'][:]:
        scan_pix.append( (data[0], data[1]) )

        sun_azi_ang.append(data[4])
        sun_ele_ang.append(data[5])
        sat_azi_ang.append(data[6])
        sat_ele_ang.append(data[7])

    ##Resizing the angle bands to the Image data size
    dst_shp = data_h5['ImageData']['B2'].shape
    sun_azi = resize(sun_azi_ang, dst_shp)
    sun_ele = resize(sun_ele_ang, dst_shp)
    sat_azi = resize(sat_azi_ang, dst_shp)
    sat_ele = resize(sat_ele_ang, dst_shp)

    return(sat_azi, sat_ele, sun_azi, sun_ele)


def resize(ang, dst_shp):
    ang_mat = np.reshape(ang, (30, 28))
    ang_img = cv2.resize(ang_mat, dst_shp, interpolation=cv2.INTER_NEAREST)
    return(ang_img)


if __name__ == '__main__':
    prod_path = pathlib.Path('Z://DQE//cvss//Resourcesat_Product//243757811_IRS-R2_L3_05-JAN-2024_STD_GEOREF_065970_099_061//BAND.h5')

    read_h5_angles(prod_path)