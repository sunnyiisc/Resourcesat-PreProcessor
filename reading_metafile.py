"""
Created on 07 Dec, 2022 at 14:36
    Title: reading_metafile.py - Reading all information form the Meta File
    Description:
        -   ...
@author: Supantha Sen, nrsc, ISRO
"""


def meta_read(file_path):
    file = open(file_path)
    meta = {}

    for line in file.readlines():
        meta[line.split('=')[0].replace(' ', '')] = line.split('=')[1].replace(' ', '').replace('\n', '')

    return(meta)


if __name__ == '__main__':
    meta = meta_read('/workspace/DQE/cvss/EOS6/RDQE_Automation/E06_OCM_GAC_05APR2023_095102453034_1883_STGO00GND_125_3_F/BAND_META.txt')
    print(meta)