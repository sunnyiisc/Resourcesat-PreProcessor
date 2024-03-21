"""
Created on 19 Mar, 2024 at 15:11
    Title: main.py - ...
    Description:
        -   ...
@author: Supantha Sen, nrsc, ISRO
"""

# Importing Modules
import pathlib

import rioxarray as rio
from affine import Affine

# Importing Custom Modules
import browse_gui

...


def main(prod_path, save_dir):

    save_path = save_dir.joinpath(prod_path.parent.stem + '.tiff')

    #data_h5 = h5.File(path, 'r')

    with rio.open_rasterio(prod_path, decode_coords='all') as dataset:
        ##Setting the CRS
        dataset.rio.write_crs('EPSG:32643', inplace=True)

        ##Setting Sparial Dimensions
        dataset.rio.set_spatial_dims(x_dim='x', y_dim='y', inplace=True)
        dataset.rio.write_coordinate_system(inplace=True)

        ##Setting Transform
        origin = (dataset.attrs['Product_ULMapX_Mtrs'], dataset.attrs['Product_ULMapY_Mtrs'])
        transform = Affine(24.0, 0.0, origin[0],
                           0.0, -24.0, origin[1])
        dataset.rio.write_transform(transform, inplace=True)

        ##Reprojecting
        # dataset = dataset.rio.reproject(dst_crs = 'EPSG:4326')

        ##Writing the Raster TIFF file
        dataset.squeeze().rio.to_raster(save_path)


if __name__ == '__main__':
    prod_path = pathlib.Path(browse_gui.browse_file('Select the HDF file to be converted'))
    save_dir = pathlib.Path(browse_gui.browse_folder('Select the Folder to save the TIFF file'))

    #path = pathlib.path('Z://DQE//cvss//Resourcesat_Product//243757811_IRS-R2_L3_05-JAN-2024_STD_GEOREF_065970_099_061//BAND.h5')
    #save_dir = pathlib.Path('Z://DQE//cvss//Resourcesat_Product')

    main(prod_path, save_dir)