#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 21:47:18 2022

@author: alexandermikhailov
"""

import datetime
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

# =============================================================================
# TODO: https://git-lfs.com
# =============================================================================
FILE_NAME = 'archive.zip' or 'urovni_p_i_n_tunguski.rar'

# =============================================================================
# DataFrames Shapes & Count:
# =============================================================================
# =============================================================================
# {
#     (5, 2): 263, # Stamps
#     (40, 13): $$$, # Core Data
#     (52, 2): 20, # Legend Same
#     (25, 2): 20, # Legend Same
#     (24, 2): 20,  # Legend Same
#     (739, 13): 2,  # Lower Tunguska :: 2014 & 2015
#     (788, 13): 2,  # Lower Tunguska :: 2016 & 2017
#     (641, 13): 2,  # Stony Tunguska :: 2014 & 2015
#     (690, 13): 2,  # Stony Tunguska :: 2016 & 2017
# }
# =============================================================================


def get_date(row):
    try:
        return datetime.date(int(row['year']), row['variable'], int(row[0]))
    except ValueError:
        return


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
        with archive.open(f'Нижняя Тунгуска {_}.xls') as f:
            df_pack = pd.read_html(f)

            for df in df_pack:
                if df.shape == (5, 2):
                    (
                        post_id, _, river_post, gauge_zero, elevation_system
                    ) = list(df.iloc[:, -1])
                elif df.shape == (40, 13):
                    df.drop(range(2), inplace=True)
                    df.drop(df.tail(7).index, inplace=True)
                    chunk = pd.melt(
                        df,
                        id_vars=df.columns[0],
                        value_vars=df.columns[1:],
                        ignore_index=False
                    )
                    chunk['year'] = _
                    chunk['location'] = 'Lower Tunguska'
                    chunk['post_id'] = post_id
                    chunk['river_post'] = river_post
                    chunk['gauge_zero'] = gauge_zero
                    chunk['elevation_system'] = elevation_system
                    dfs.append(chunk)

    for _ in range(2008, 2018):
        with archive.open(f'Подкаменная Тунгуска {_}.xls') as f:
            df_pack = pd.read_html(f)

            for df in df_pack:
                if df.shape == (5, 2):
                    (
                        post_id, _, river_post, gauge_zero, elevation_system
                    ) = list(df.iloc[:, -1])
                elif df.shape == (40, 13):
                    df.drop(range(2), inplace=True)
                    df.drop(df.tail(7).index, inplace=True)
                    chunk = pd.melt(
                        df,
                        id_vars=df.columns[0],
                        value_vars=df.columns[1:],
                        ignore_index=False
                    )
                    chunk['year'] = _
                    chunk['location'] = 'Stony Tunguska'
                    chunk['post_id'] = post_id
                    chunk['river_post'] = river_post
                    chunk['gauge_zero'] = gauge_zero
                    chunk['elevation_system'] = elevation_system
                    dfs.append(chunk)

    df = pd.concat(dfs)

    df['date'] = df.apply(get_date, axis=1)
    df.dropna(inplace=True)
    df['gauge_zero'] = df['gauge_zero'].apply(pd.to_numeric)

    df.drop(df.columns[range(2)], axis=1, inplace=True)
    df.drop(df.columns[range(1, 2)], axis=1, inplace=True)

    columns_shuffled = [
        'location',
        'river_post',
        'post_id',
        'elevation_system',
        'date',
        'gauge_zero',
        'value'
    ]

# =============================================================================
# TODO: Split `value`
# =============================================================================
