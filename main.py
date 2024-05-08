"""
Created on 19 Mar, 2024 at 15:11
    Title: main.py - ...
    Description:
        -   ...
@author: Supantha Sen, nrsc, ISRO
"""

# Importing Modules
import pathlib

import numpy as np
import xarray as xr
import rasterio
import rioxarray as rio
from affine import Affine

# Importing Custom Modules
import browse_gui
from reading_h5 import read_h5_angles
import reading_metafile

...


def main(prod_path, save_dir):

    meta = reading_metafile.meta_read( prod_path.parent.joinpath('BAND_META.txt') )


    with rio.open_rasterio(prod_path, engine='h5netcdf') as dataset:
        ##Extracting Image Meta Parameters
        origin = (float(dataset.attrs['Product_ULMapX_Mtrs']), float(dataset.attrs['Product_ULMapY_Mtrs']))
        res = (float(dataset.attrs['OutputResolution_Across_mtrs']), float(dataset.attrs['OutputResolution_Along_mtrs']))
        projection = dataset.attrs['Map_Projection_Parameters_Map_Projection']
        zone = dataset.attrs['Map_Projection_Parameters_Projection_Parameter_03']

        ##Setting the CRS
        if projection == 'UniverseTransverseMercator':
            crs = 'EPSG:' + '326' + str(zone)
        dataset.rio.write_crs(crs, inplace=True)

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
        (x_val, y_val) = (dataset.x.values - 0.5, dataset.y.values - 0.5)
        row = transformer.xy(y_val, 0)[1]
        col = transformer.xy(0, x_val)[0]

        dataset = dataset.assign_coords({'x':col, 'y':row})

        ##Adding Angle Bands
        sat_azi, sat_ele, sun_azi, sun_ele = read_h5_angles(prod_path)
        dataset['Sun_Azi_Band'] = xr.DataArray(sun_azi.reshape(1, len(row), len(col)), coords=dataset.coords,
                                               dims=dataset.dims, name='Sun_Azi_Band')
        dataset['Sun_Zn_Band'] = xr.DataArray(sun_ele.reshape(1, len(row), len(col)), coords=dataset.coords,
                                               dims=dataset.dims, name='Sun_Zn_Band')
        dataset['Sat_Azi_Band'] = xr.DataArray(sat_azi.reshape(1, len(row), len(col)), coords=dataset.coords,
                                               dims=dataset.dims, name='Sat_Azi_Band')
        dataset['Sat_Zn_Band'] = xr.DataArray(sat_ele.reshape(1, len(row), len(col)), coords=dataset.coords,
                                               dims=dataset.dims, name='Sat_Zn_Band')
        for band in dataset:
            if band.startswith('S'):
                dataset[band].attrs['scale_factor'] = 0.01


        ##Writing the Raster TIFF file
        print('Writing DN file ... with angle bands scaling factor as 0.01 ...')
        save_path_dn = save_dir.joinpath(prod_path.parent.stem + '.tiff')
        dataset.squeeze().rio.to_raster(save_path_dn)
        print('DN file written at ',save_path_dn)

if __name__ == '__main__':
    prod_path = pathlib.Path(browse_gui.browse_file('Select the HDF file to be converted'))
    save_dir = pathlib.Path(browse_gui.browse_folder('Select the Folder to save the TIFF file'))

    main(prod_path, save_dir)
