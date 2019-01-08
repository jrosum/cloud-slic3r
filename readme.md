[![Build Status](https://travis-ci.org/jrosum/cloud-slic3r.svg?branch=master)](https://travis-ci.org/jrosum/cloud-slic3r)
# slic3r web frontend

web frontend based on [Slic3r](https://slic3r.org/), the open source 3D printing toolbox.

## Prerequisites

### Mac

Install slic3r for Mac: http://macappstore.org/slic3r/
```
$ cp -rf /Applications/Slic3r.app/Contents/MacOS/* /usr/local/bin
```

And following tools:

```
$ brew install povray admesh
```

### Linux

```
$ apt-get install -y slic3r povray admesh
```

## Run

```
cd src
pip3 install -r requirements.txt
python3 main.py
````
