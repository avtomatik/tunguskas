#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 21:47:18 2022

@author: alexandermikhailov
"""

from pathlib import Path
from zipfile import ZipFile

import pandas as pd

# =============================================================================
# TODO: https://git-lfs.com
# =============================================================================
FILE_NAME = 'urovni_p_i_n_tunguski.rar'
FILE_NAME = 'archive.zip'


with ZipFile(
    (
        Path(__file__).parent.parent
        .joinpath('data')
        .joinpath('raw')
        .joinpath(FILE_NAME)
    )
) as archive:

    dfs = []

    with archive.open('!Уровни постов.xlsx') as f:
        df_streamgages = pd.read_excel(f)

    for _ in range(2008, 2018):
        df_pack = pd.read_html(archive.open(f'Нижняя Тунгуска {_}.xls'))
        for df in df_pack:
            dfs.append(df)

    for _ in range(2008, 2018):
        df_pack = pd.read_html(archive.open(f'Подкаменная Тунгуска {_}.xls'))
        for df in df_pack:
            dfs.append(df)

print(df_streamgages)
print(len(dfs))
