"""
Created on 19 Mar, 2024 at 15:11
    Title: main.py - ...
    Description:
        -   ...
@author: Supantha Sen, nrsc, ISRO
"""

# Importing Modules
import pathlib
import rasterio
import xarray as xr
import rioxarray as rio
import h5py as h5

# Importing Custom Modules
import browse_gui

...


def main(prod_path, save_dir):

    save_path = save_dir.joinpath(prod_path.parent.stem + '.tiff')

    #data_h5 = h5.File(path, 'r')

    with rio.open_rasterio(prod_path) as dataset:
        #dataset.rio.write_crs('EPSG:32643', inplace=True)
        #dataset = dataset.rio.reproject(dst_crs = 'EPSG:32643')
        dataset.rio.set_spatial_dims(x_dim = 'x', y_dim = 'y', inplace=True)
        dataset.squeeze().rio.to_raster(save_path, recalc_tranform = False)


if __name__ == '__main__':
    prod_path = pathlib.Path(browse_gui.browse_file('Select the HDF file to be converted'))
    save_dir = pathlib.Path(browse_gui.browse_folder('Select the Folder to save the TIFF file'))

    #path = pathlib.path('Z://DQE//cvss//Resourcesat_Product//243757811_IRS-R2_L3_05-JAN-2024_STD_GEOREF_065970_099_061//BAND.h5')
    #save_dir = pathlib.Path('Z://DQE//cvss//Resourcesat_Product')

    main(prod_path, save_dir)