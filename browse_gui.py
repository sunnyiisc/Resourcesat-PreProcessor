"""
Created on 30 Aug, 2022 at 11:24
    Title: browse_gui.py - Browsing GUI for selecting Folders and Files
    Description:
        -   ...
@author: Supantha Sen, nrsc, ISRO
"""

# Importing Modules
from tkinter import filedialog

# Importing Custom Modules
...

...

def browse_folder(title_name):
    directory = filedialog.askdirectory(initialdir = '/workspace/DQE/cvss',
                                        title = title_name
                                       )
    return directory


def browse_file(title_name):
    filename = filedialog.askopenfilename(initialdir = '/workspace/DQE/cvss',
                                          title = title_name,
                                          filetypes = (('all files','*.*'), ('text files', '*.txt*'))
                                         )
    return filename