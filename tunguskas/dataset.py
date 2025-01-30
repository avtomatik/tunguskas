#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 21:47:18 2022

@author: alexandermikhailov
"""

import datetime
import re
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

from .config import COLUMNS_RE_SHUFFLED, FILE_NAME, SHAPE_DATA, SHAPE_STAMPS


def get_date(row):
    try:
        return datetime.date(int(row['year']), row['variable'], int(row[0]))
    except ValueError:
        return


def swap_value(value):
    match = re.search(r'(?P<legend>\D+) (?P<reading>\d+)', value)
    if match:
        return f"{match.group('reading')} {match.group('legend')}"
    return value


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

    for year in range(2008, 2018):
        with archive.open(f'Нижняя Тунгуска {year}.xls') as f:
            location = 'Lower Tunguska'
            df_pack = pd.read_html(f)

            for chunk in df_pack:
                if chunk.shape == SHAPE_STAMPS:
                    post_id, _, river_post, gauge_zero, _ = chunk.iloc[:, -1]
                elif chunk.shape == SHAPE_DATA:
                    chunk.drop(range(2), inplace=True)
                    chunk.drop(chunk.tail(7).index, inplace=True)
                    df = pd.melt(
                        chunk,
                        id_vars=chunk.columns[0],
                        value_vars=chunk.columns[1:],
                        ignore_index=False
                    )
                    df['year'] = year
                    df['location'] = location
                    df['post_id'] = post_id
                    df['river_post'] = river_post
                    df['gauge_zero'] = gauge_zero
                    dfs.append(df)

    for year in range(2008, 2018):
        with archive.open(f'Подкаменная Тунгуска {year}.xls') as f:
            location = 'Stony Tunguska'
            df_pack = pd.read_html(f)

            for chunk in df_pack:
                if chunk.shape == SHAPE_STAMPS:
                    post_id, _, river_post, gauge_zero, _ = chunk.iloc[:, -1]
                elif chunk.shape == SHAPE_DATA:
                    chunk.drop(range(2), inplace=True)
                    chunk.drop(chunk.tail(7).index, inplace=True)
                    df = pd.melt(
                        chunk,
                        id_vars=chunk.columns[0],
                        value_vars=chunk.columns[1:],
                        ignore_index=False
                    )
                    df['year'] = year
                    df['location'] = location
                    df['post_id'] = post_id
                    df['river_post'] = river_post
                    df['gauge_zero'] = gauge_zero
                    dfs.append(df)

    df = pd.concat(dfs)

    df['date'] = df.apply(get_date, axis=1)

    df.dropna(inplace=True)

    df['gauge_zero'] = df['gauge_zero'].apply(pd.to_numeric)
    df['value'] = df['value'].apply(swap_value)

    df.drop(df.columns[range(2)], axis=1, inplace=True)
    df.drop(df.columns[range(1, 2)], axis=1, inplace=True)

    df[['value', 'legend']] = df['value'].str.extract(
        r'(?P<reading>\d+)(?P<legend> \D+)?',
        expand=True
    )

    df['legend'] = df['legend'].str.strip()
    df['value'] = df['value'].apply(pd.to_numeric, downcast='integer')

    df[COLUMNS_RE_SHUFFLED].to_csv(
        (
            Path(__file__).parent.parent
            .joinpath('data')
            .joinpath('processed')
            .joinpath('dataset.csv')
        ),
        index=False
    )
