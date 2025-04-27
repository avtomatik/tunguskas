#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 21:47:18 2022

@author: alexandermikhailov
"""

import datetime
import re
import zipfile

import pandas as pd
from config import COLUMNS_RE_SHUFFLED, DATA_DIR, FILE_NAME, Shape


def get_date(row: pd.Series):
    try:
        return datetime.date(int(row['year']), row['variable'], int(row[0]))
    except ValueError:
        return


def swap_value(value: str) -> str:
    match = re.search(r'(?P<legend>\D+) (?P<reading>\d+)', value)
    if match:
        return f"{match.group('reading')} {match.group('legend')}"
    return value


def process_file(
    archive: zipfile.ZipFile,
    location: str,
    year: int
) -> list[pd.DataFrame]:
    dfs = []

    with archive.open(f'{location} {year}.xls') as f:
        df_pack = pd.read_html(f)

        for chunk in df_pack:
            if chunk.shape == Shape.STAMPS.value:
                post_id, _, river_post, gauge_zero, _ = chunk.iloc[:, -1]
            elif chunk.shape == Shape.DATA.value:
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

    return dfs


def process_archive(archive: zipfile.ZipFile) -> pd.DataFrame:
    all_dfs = []

    location = 'Нижняя Тунгуска'
    for year in range(2008, 2018):
        all_dfs.extend(process_file(archive, location, year))

    location = 'Подкаменная Тунгуска'
    for year in range(2008, 2018):
        all_dfs.extend(process_file(archive, location, year))

    return pd.concat(all_dfs)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
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

    return df


def save_processed_data(df: pd.DataFrame) -> None:
    df[COLUMNS_RE_SHUFFLED].to_csv(
        DATA_DIR.joinpath('processed').joinpath('dataset.csv'),
        index=False
    )


def main():
    with zipfile.ZipFile(
        DATA_DIR.joinpath('raw').joinpath(FILE_NAME)
    ) as archive:
        (
            process_archive(archive)
            .pipe(clean_data)
            .pipe(save_processed_data)
        )


if __name__ == '__main__':
    main()
