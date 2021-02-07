# tja-download

![License: GPLv3](https://img.shields.io/badge/License-GPLv3-green.svg)
![python 3.5+](https://img.shields.io/badge/python-3.5+-blue)

These scripts dump tja file download links, download archives from the dumped links, and extract the zip files downloaded.

## TODO

- Thorough testing.

- `rar` extraction.

- Optimization.

## Set up environment

```
python3 -m venv venv
source bin/venv/activate
pip3 install -r requirements.txt
```

## Dump links

(inside the virtual environment)

```
python3 dump_links.py
```

The download links will be saved in csv format in the `links` directory. The csv files generated are in the format of `filename`, `comment`, `link` without a heading row.

## Download archives

(inside the virtual environment)

```
python3 download.py
```

The downloaded files will be stored in the `downloads` directory. Files are put into `本家` and `others` subdirectories according to whether `本家` is presented in the `comment` column of the csv files. Links where this script fail to download a file will be outputted at the end of execution.

## Extract

(inside the virtual environment)

```
python3 extract.py
```

The extracted files will be stored in the `extracted` directory. `zip` files will be extracted, `mp3`, `ogg`, and `tja` files will be copied, and other files will be ignored. The files in the `zip` archives will be properly re-coded from `shiftjs` encoding. Files this script fail to extract or copy will be outputted at the end of execution.
