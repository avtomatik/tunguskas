# Source Data

## Archive format

The source archive contains historical hydrological observations
for Lower Tunguska and Stony Tunguska.

## HTML table shapes

| Shape | Meaning |
|---|---|
| (5, 2) | Station metadata |
| (40, 13) | Core observation data |
| (52, 2) | Legend |
| (25, 2) | Legend |
| (24, 2) | Legend |

## Known irregularities

| Shape | Location | Years |
|---|---|---|
| (739, 13) | Lower Tunguska | 2014–2015 |
| (788, 13) | Lower Tunguska | 2016–2017 |
| (641, 13) | Stony Tunguska | 2014–2015 |
| (690, 13) | Stony Tunguska | 2016–2017 |

## TODO

- Investigate Git LFS for large source archives.
- Find a suitable tool for reading RAR archives.
