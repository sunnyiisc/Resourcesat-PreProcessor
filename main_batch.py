"""
Created on 10 May, 2024 at 12:48
    Title: main_batch.py - Conversion of HDF to Georeferenced Band Stacked TIFF file in batch mode
    Description:
        -   Running the 'h5' to 'tiff' with georeferencing in batch mode.
@author: Supantha Sen, nrsc, ISRO
"""

# Importing Modules

# Importing Custom Modules
from main import *
import browse_gui

...
dataset_path = pathlib.Path(browse_gui.browse_folder('Select the directory containing all the product folders'))

save_dir = pathlib.Path(browse_gui.browse_folder('Select the Folder to save the TIFF file'))

prod = list([x for x in dataset_path.glob('*/') if x.is_dir()])
for product_path in prod:
    main(product_path, save_dir)

    index = prod.index(product_path)+1
    print('Completed = '+str((index*100)/len(prod))+'%\n')