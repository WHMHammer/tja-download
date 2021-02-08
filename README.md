# tja-download

![License: GPLv3](https://img.shields.io/badge/License-GPLv3-green.svg)
![Python 3.6+](https://img.shields.io/badge/Python-3.6+-blue)

These scripts dump tja file download links, download archives from the dumped links, and extract the zip files downloaded.

## TODO

- `rar` extraction.

## Requirement

- Python 3.8+

## Notice

If you are planning to modify my code to boost download by multiprocessing/threading: DON'T do it. It will cause your ip to be banned by `ux.getuploader.com`.

Use or modify my code AT YOUR OWN RISK for This project is released under GPLv3. Below is an excerption from the license:

```
  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.
```

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
