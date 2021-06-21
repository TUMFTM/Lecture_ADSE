<p align="center">
<img src="https://raw.githubusercontent.com/xdspacelab/openvslam/master/docs/img/logo.png" width="435px">
</p>

# OpenVSLAM: A Versatile Visual SLAM Framework

https://github.com/xdspacelab/openvslam

# Installation

## Ubuntu (tested on 18.04)

Install dependencies:

```
apt update -y
apt upgrade -y --no-install-recommends
# basic dependencies
apt install -y build-essential pkg-config cmake git wget curl unzip
# g2o dependencies
apt install -y libatlas-base-dev libsuitesparse-dev
# OpenCV dependencies
apt install -y libgtk-3-dev
apt install -y ffmpeg
apt install -y libavcodec-dev libavformat-dev libavutil-dev libswscale-dev libavresample-dev
# eigen dependencies
apt install -y gfortran
# other dependencies
apt install -y libyaml-cpp-dev libgoogle-glog-dev libgflags-dev
# Pangolin dependencies
apt install -y libglew-dev
```

Move into vSLAM directory:

```
cd /path/to/mod_map_loc/vSLAM
```

Download and install Eigen from source:

```
wget -q https://gitlab.com/libeigen/eigen/-/archive/3.3.7/eigen-3.3.7.tar.bz2
tar xf eigen-3.3.7.tar.bz2
rm -rf eigen-3.3.7.tar.bz2
cd eigen-3.3.7
mkdir -p build && cd build
cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local \
    ..
make -j4
sudo make install
cd ../..
```

Download, build and install OpenCV from source:

```
wget -q https://github.com/opencv/opencv/archive/3.4.0.zip
unzip -q 3.4.0.zip
rm -rf 3.4.0.zip
cd opencv-3.4.0
mkdir -p build && cd build
cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local \
    -DENABLE_CXX11=ON \
    -DBUILD_DOCS=OFF \
    -DBUILD_EXAMPLES=OFF \
    -DBUILD_JASPER=OFF \
    -DBUILD_OPENEXR=OFF \
    -DBUILD_PERF_TESTS=OFF \
    -DBUILD_TESTS=OFF \
    -DWITH_EIGEN=ON \
    -DWITH_FFMPEG=ON \
    -DWITH_OPENMP=ON \
    ..
make -j4
sudo make install
cd ../..
```

Download, build and install the custom DBoW2 from source:

```
git clone https://github.com/shinsumicco/DBoW2.git
cd DBoW2
mkdir build && cd build
cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local \
    ..
make -j4
sudo make install
cd ../..
```

Download, build and install g2o:

```
git clone https://github.com/RainerKuemmerle/g2o.git
cd g2o
git checkout 9b41a4ea5ade8e1250b9c1b279f3a9c098811b5a
mkdir build && cd build
cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local \
    -DCMAKE_CXX_FLAGS=-std=c++11 \
    -DBUILD_SHARED_LIBS=ON \
    -DBUILD_UNITTESTS=OFF \
    -DBUILD_WITH_MARCH_NATIVE=ON \
    -DG2O_USE_CHOLMOD=OFF \
    -DG2O_USE_CSPARSE=ON \
    -DG2O_USE_OPENGL=OFF \
    -DG2O_USE_OPENMP=ON \
    ..
make -j4
sudo make install
cd ../..
```

Download, build and install Pangolin from source:

```
git clone https://github.com/stevenlovegrove/Pangolin.git
cd Pangolin
git checkout ad8b5f83222291c51b4800d5a5873b0e90a0cf81
mkdir build && cd build
cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local \
    ..
make -j4
sudo make install
cd ../..
```

Build OpenVSLAM:

```
cd openvslam
mkdir build && cd build
cmake \
    -DBUILD_WITH_MARCH_NATIVE=ON \
    -DUSE_PANGOLIN_VIEWER=ON \
    -DUSE_SOCKET_PUBLISHER=OFF \
    -DUSE_STACK_TRACE_LOGGER=ON \
    -DBOW_FRAMEWORK=DBoW2 \
    -DBUILD_TESTS=ON \
    ..
make -j4
```

Download an ORB vocabulary file from Google Drive:

```
# inside 'vSLAM/openvslam/build'
FILE_ID="1wUPb328th8bUqhOk-i8xllt5mgRW4n84"
curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=${FILE_ID}" > /dev/null
CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
curl -sLb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=${FILE_ID}" -o orb_vocab.zip
unzip orb_vocab.zip
```

## Windows and OSX

Please check [**OpenVSLAM documentation**](https://openvslam.readthedocs.io/en/master/installation.html) for detailed instructions.



# Run OpenVSLAM

Run SLAM with example data:

```
# Download a sample dataset from Google Drive

# inside 'vSLAM/openvslam/build'
FILE_ID="1d8kADKWBptEqTF7jEVhKatBEdN7g0ikY"
curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=${FILE_ID}" > /dev/null
CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
curl -sLb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=${FILE_ID}" -o aist_living_lab_1.zip
unzip aist_living_lab_1.zip

# Run SLAM

./run_video_slam -v ./orb_vocab/orb_vocab.dbow2 -m ./aist_living_lab_1/video.mp4 -c ./aist_living_lab_1/config.yaml --frame-skip 3 --no-sleep --map-db map.msg
# click the [Terminate] button to close the viewer
# you can find map.msg in the current directory
```

FTM simulator

Run SLAM with FTM simulator data:

```
# inside 'vSLAM/openvslam/build'
./run_image_slam -v orb_vocab/orb_vocab.dbow2 -i /path/to/images -c ../example/iac/config_ftm.yaml
```

Run SLAM with FTM simulator data and save map:

```
# inside 'vSLAM/openvslam/build'
./run_image_slam -v orb_vocab/orb_vocab.dbow2 -i /path/to/images -c ../example/iac/config_ftm.yaml -p /path/to/map.msg
```

Run (1D) Localization with FTM simulator data on saved map:

```
# inside 'vSLAM/openvslam/build'
./run_image_localization -v orb_vocab/orb_vocab.dbow2 -i /path/to/images -c ../example/iac/config_ftm.yaml -p /path/to/map.msg
```

Run SLAM with FTM simulator data and use ground truth data to improve mapping (not stable):

```
# inside 'vSLAM/openvslam/build'
./run_iac_image_gps_slam -v orb_vocab/orb_vocab.dbow2 -i /path/to/images -c ../example/iac/config_ftm.yaml -g /path/to/IMU_100Hz.csv
```

Project Cars 2
Videos and pre-generated maps can be found at https://webdisk.ads.mwn.de/Default.aspx?folder=TUMW%2Fftm%2FRoborace%2F11_Students%2FStudenten_Sauerbeck%2FJulius_Drosten%2FProject_Cars

- project_cars_1.mp4: fast driving
- project_cars_2.mp4: slow driving, best for generating maps
- project_cars_3.mp4: constant driving at 120 km/h

Run SLAM with Project Cars 2 video and save new map:

```
# inside 'vSLAM/openvslam/build'
./run_video_slam -v orb_vocab/orb_vocab.dbow2 -m /path/to/project_cars_2.mp4 -c ../example/iac/config_project_cars.yaml -p /path/to/project_cars_map.msg
```

Run (1D) Localization with Project Cars 2 video on saved map:

```
# inside 'vSLAM/openvslam/build'
./run_video_localization -v orb_vocab/orb_vocab.dbow2 -m /path/to/project_cars_3.mp4 -c ../example/iac/config_project_cars.yaml -p /path/to/project_cars_map.msg
```

On-board video
https://www.youtube.com/watch?v=a4EmOUaXL1I

Run SLAM with on-board video and save new map:

# inside 'vSLAM/openvslam/build'
./run_video_slam -v orb_vocab/orb_vocab.dbow2 -m /path/to/on_board_video.mp4 -c ../example/iac/config_youtube.yaml -p /path/to/on_board_video_map.msg

Run (1D) Localization with on-board video on saved map:

# inside 'vSLAM/openvslam/build'
./run_video_localization -v orb_vocab/orb_vocab.dbow2 -m /path/to/on_board_video.mp4 -c ../example/iac/config_youtube.yaml -p /path/to/on_board_video_map.msg

# License

**2-clause BSD license** (see [LICENSE](./LICENSE))

The following files are derived from third-party libraries.

- `./3rd/json` : [nlohmann/json \[v3.6.1\]](https://github.com/nlohmann/json) (MIT license)
- `./3rd/popl` : [badaix/popl \[v1.2.0\]](https://github.com/badaix/popl) (MIT license)
- `./3rd/spdlog` : [gabime/spdlog \[v1.3.1\]](https://github.com/gabime/spdlog) (MIT license)
- `./src/openvslam/solver/pnp_solver.cc` : part of [laurentkneip/opengv](https://github.com/laurentkneip/opengv) (3-clause BSD license)
- `./src/openvslam/feature/orb_extractor.cc` : part of [opencv/opencv](https://github.com/opencv/opencv) (3-clause BSD License)
- `./src/openvslam/feature/orb_point_pairs.h` : part of [opencv/opencv](https://github.com/opencv/opencv) (3-clause BSD License)
- `./viewer/public/js/lib/dat.gui.min.js` : [dataarts/dat.gui](https://github.com/dataarts/dat.gui) (Apache License 2.0)
- `./viewer/public/js/lib/protobuf.min.js` : [protobufjs/protobuf.js](https://github.com/protobufjs/protobuf.js) (3-clause BSD License)
- `./viewer/public/js/lib/stats.min.js` : [mrdoob/stats.js](https://github.com/mrdoob/stats.js) (MIT license)
- `./viewer/public/js/lib/three.min.js` : [mrdoob/three.js](https://github.com/mrdoob/three.js) (MIT license)

Please use `g2o` as the dynamic link library because `csparse_extension` module of `g2o` is LGPLv3+.

# Contributors

- Shinya Sumikura ([@shinsumicco](https://github.com/shinsumicco))
- Mikiya Shibuya ([@MikiyaShibuya](https://github.com/MikiyaShibuya))
- Ken Sakurada ([@kensakurada](https://github.com/kensakurada))

# Citation

OpenVSLAM **won first place** at **ACM Multimedia 2019 Open Source Software Competition**.

If OpenVSLAM helps your research, please cite the paper for OpenVSLAM. Here is a BibTeX entry:

```
@inproceedings{openvslam2019,
  author = {Sumikura, Shinya and Shibuya, Mikiya and Sakurada, Ken},
  title = {{OpenVSLAM: A Versatile Visual SLAM Framework}},
  booktitle = {Proceedings of the 27th ACM International Conference on Multimedia},
  series = {MM '19},
  year = {2019},
  isbn = {978-1-4503-6889-6},
  location = {Nice, France},
  pages = {2292--2295},
  numpages = {4},
  url = {http://doi.acm.org/10.1145/3343031.3350539},
  doi = {10.1145/3343031.3350539},
  acmid = {3350539},
  publisher = {ACM},
  address = {New York, NY, USA}
}
```

The preprint can be found [here](https://arxiv.org/abs/1910.01122).

# Reference

- Raúl Mur-Artal, J. M. M. Montiel, and Juan D. Tardós. 2015. ORB-SLAM: a Versatile and Accurate Monocular SLAM System. IEEE Transactions on Robotics 31, 5 (2015), 1147–1163.
- Raúl Mur-Artal and Juan D. Tardós. 2017. ORB-SLAM2: an Open-Source SLAM System for Monocular, Stereo and RGB-D Cameras. IEEE Transactions on Robotics 33, 5 (2017), 1255–1262.
- Dominik Schlegel, Mirco Colosi, and Giorgio Grisetti. 2018. ProSLAM: Graph SLAM from a Programmer’s Perspective. In Proceedings of IEEE International Conference on Robotics and Automation (ICRA). 1–9.
- Rafael Muñoz-Salinas and Rafael Medina Carnicer. 2019. UcoSLAM: Simultaneous Localization and Mapping by Fusion of KeyPoints and Squared Planar Markers. arXiv:1902.03729.
- Mapillary AB. 2019. OpenSfM. https://github.com/mapillary/OpenSfM.
- Giorgio Grisetti, Rainer Kümmerle, Cyrill Stachniss, and Wolfram Burgard. 2010. A Tutorial on Graph-Based SLAM. IEEE Transactions on Intelligent Transportation SystemsMagazine 2, 4 (2010), 31–43.
- Rainer Kümmerle, Giorgio Grisetti, Hauke Strasdat, Kurt Konolige, and Wolfram Burgard. 2011. g2o: A general framework for graph optimization. In Proceedings of IEEE International Conference on Robotics and Automation (ICRA). 3607–3613.
