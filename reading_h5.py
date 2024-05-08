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
    sun_azi = (resize(scan_pix, sun_azi_ang, dst_shp) * 1e2).astype('uint16')
    sun_ele = ((90.0 - resize(scan_pix, sun_ele_ang, dst_shp)) * 1e2).astype('uint16')
    sat_azi = (resize(scan_pix, sat_azi_ang, dst_shp) * 1e2).astype('uint16')
    sat_ele = ((90 - resize(scan_pix, sat_ele_ang, dst_shp)) * 1e2).astype('uint16')

    return(sat_azi, sat_ele, sun_azi, sun_ele)


def resize(scan_pix, ang, dst_shp):
    ##Getting the size of the angle band given
    sampling_size = scan_pix[1][1]
    size_scan_pix = (scan_pix[-1] / sampling_size) + 1
    size_xy = tuple( size_scan_pix.astype('int') )

    ## Creating the angle bands to 2D and interpolating to image size
    ang_mat = np.reshape(ang, size_xy)     ##size_xy is RS2=(28, 30), RS2A=(14, 16)
    ang_img = cv2.resize(ang_mat, dst_shp[::-1], interpolation=cv2.INTER_NEAREST)
    return(ang_img)


if __name__ == '__main__':
    prod_path = pathlib.Path('C://Users//Supantha_Sen//Desktop//share//Satellite_Data//Resourcesat//243757811_IRS-R2_L3_05-JAN-2024_STD_GEOREF_065970_099_061//BAND.h5')

    read_h5_angles(prod_path)
