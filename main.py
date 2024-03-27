"""
Created on 19 Mar, 2024 at 15:11
    Title: main.py - ...
    Description:
        -   ...
@author: Supantha Sen, nrsc, ISRO
"""

# Importing Modules
import pathlib
import h5py
import rasterio
import rioxarray as rio
from affine import Affine

# Importing Custom Modules
import browse_gui

...


def main(prod_path, save_dir):

    save_path = save_dir.joinpath(prod_path.parent.stem + '.tiff')

    #data_h5 = h5.File(path, 'r')

    with rio.open_rasterio(prod_path, engine='h5netcdf') as dataset:
        ##Extracting Image Meta Parameters
        origin = (float(dataset.attrs['Product_ULMapX_Mtrs']), float(dataset.attrs['Product_ULMapY_Mtrs']))
        res = (float(dataset.attrs['InputResolution_Across_mtrs']), float(dataset.attrs['InputResolution_Along_mtrs']))

        ##Setting the CRS
        dataset.rio.write_crs('EPSG:32643', inplace=True)

        ##Setting Sparial Dimensions
        dataset.rio.set_spatial_dims(x_dim='x', y_dim='y', inplace=True)
        dataset.rio.write_coordinate_system(inplace=True)

        ##Setting Transform
        transform = Affine( res[0], 0.0, origin[0],
                            0.0, -res[1], origin[1] )

        transformer = rasterio.transform.AffineTransformer(transform)
        dataset.rio.write_transform(transform, inplace=True)

        ##Reprojecting
        #dataset_reproj = dataset.rio.reproject(dst_crs = 'EPSG:4326')

        ##Setting Coords
        (x_val, y_val) = (dataset.x.values, dataset.y.values)
        row = transformer.xy(y_val, 0)[1]
        col = transformer.xy(0, x_val)[0]

        dataset = dataset.assign_coords({'x':col, 'y':row})

        ##Writing the Raster TIFF file
        dataset.squeeze().rio.to_raster(save_path)
        #dataset_reproj.squeeze().rio.to_raster(save_dir.joinpath(prod_path.parent.stem + '_reproj' + '.tiff'))

if __name__ == '__main__':
    #prod_path = pathlib.Path(browse_gui.browse_file('Select the HDF file to be converted'))
    #save_dir = pathlib.Path(browse_gui.browse_folder('Select the Folder to save the TIFF file'))

    prod_path = pathlib.Path('Z://DQE//cvss//Resourcesat_Product//243757811_IRS-R2_L3_05-JAN-2024_STD_GEOREF_065970_099_061//BAND.h5')
    save_dir = pathlib.Path('Z://DQE//cvss//Resourcesat_Product')

    main(prod_path, save_dir)