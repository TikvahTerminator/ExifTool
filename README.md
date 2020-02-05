# ExifTool

ExifTool is a python tool for digital investigation of EXIF Geo-Location data from photos.

## Installation

Clone into this repo or download via a browser.

```bash
git clone https://github.com/TikvahTerminator/ExifTool.git
```

ExifTool has the following dependencies:
- [ExifRead](https://pypi.org/project/ExifRead/)
- [Folium](https://pypi.org/project/folium/)
- [Pillow](https://pypi.org/project/Pillow/)
- [HashLib](https://docs.python.org/3/library/hashlib.html)
- [Matplotlib](https://matplotlib.org/)


## Usage

Please note that ExifTool is built in Python 3. 

Run the following inside the git cloned repo (ensuring you have requirements.txt)

```bash
python -m pip install -r requirements.txt
python ExifTool.py [Directory of photos]
```

ExifTool will drop a "Map.html" in the Current Working Directory.

## Layout
![Alt](https://i.imgur.com/3Xdj3ik.png "Demonstrative Image")

ExifTool will generate plots with the following data:

- Date of image creation
- Time of image creation
- Latitude of image
- Longitude of image
- SHA-512 Hash of image
- MD5 Hash of image
- Image Name
- Actual image!
