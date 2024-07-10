![nvblox](docs/images/nvblox_logo_64.png)

![Signed Distance Functions (SDFs) on NVIDIA GPUs](docs/images/3dmatch.gif)

A GPU SDF library which offers
* GPU accelerated algorithms such as:
  * TSDF construction
  * Occupancy mapping
  * ESDF construction
  * Meshing
* ROS 2 interface (see [isaac_ros_nvblox](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_nvblox))
* Support for storage of various voxel types, and easily extended to custom voxel types.

Above we show reconstruction using data from the [3DMatch dataset](https://3dmatch.cs.princeton.edu/), specifically the [Sun3D](http://sun3d.cs.princeton.edu/) `mit_76_studyroom` scene. 

## Table of Contents

- [Why nvblox? ](#why-nvblox)
- [How to use nvblox ](#how-to-use-nvblox)
  - [Out-of-the-box Reconstruction/ROS 2 Interface ](#out-of-the-box-reconstructionros-2-interface)
  - [Public Datasets ](#public-datasets)
  - [C++ Interface ](#c-interface)
- [Native Installation ](#native-installation)
  - [Install dependencies ](#install-dependencies)
  - [Build and run tests and benchmark ](#build-and-run-tests-and-benchmark)
  - [Run an example ](#run-an-example)
- [Docker ](#docker)
- [Open3D on Jetson ](#open3d-on-jetson)
- [Building for multiple GPU architectures ](#building-for-multiple-gpu-architectures)
- [Building redistributable binaries, with static dependencies ](#building-redistributable-binaries-with-static-dependencies)
- [License ](#license)
- [Paper ](#paper)



# Why nvblox? <a id='why-nvblox'></a>

Do we need another SDF library? That depends on your use case. If you're interested in:
* **Path planning**: We provide GPU accelerated, incremental algorithms for calculating the Euclidean Signed Distance Field (ESDF) which is useful for collision checking for robotic path-planning.
* **GPU acceleration**: Our previous works [voxblox](https://github.com/ethz-asl/voxblox) and [voxgraph](https://github.com/ethz-asl/voxgraph) are used for path-planning, however utilize CPU compute only, which limits the speed of these toolboxes, and therefore the resolution of the maps they can build in real-time. nvblox is *much* faster.
* **Jetson Platform**: nvblox is written with the [NVIDIA jetson](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/) in mind. If you want to run reconstruction on an embedded GPU, you're in the right place.

Below we visualize slices through a distance function (ESDF):

![](docs/images/nvblox_slice.gif)


# How to use nvblox <a id='how-to-use-nvblox'></a>
How use nvblox depends on what you want to do. 

## Out-of-the-box Reconstruction/ROS 2 Interface <a id='out-of-the-box-reconstructionros-2-interface'></a>

For users who would like to use nvblox in a robotic system or connect easily to a sensor, we suggest using our [ROS 2 interface](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_nvblox).

The ROS 2 interface includes examples which allow you to:
* Build a reconstruction from a Realsense camera using nvblox and NVIDIA VSLAM
* Navigate a robot in Isaac Sim
* Combine 3D reconstruction with image segmentation with realsense data and in simulation

The ROS 2 interface downloads and builds the library contained in this repository during installation, so you don't need to clone and build this repository at all.

## Public Datasets <a id='public-datasets'></a>

If you would like to run nvblox on a public datasets, we include some executables for running reconstructions on [3DMatch](https://3dmatch.cs.princeton.edu/), [Replica](https://github.com/facebookresearch/Replica-Dataset), and [Redwood](http://redwood-data.org/indoor_lidar_rgbd/index.html) datasets. Please see our [tutorial](docs/pages/tutorial_public_datasets.md) on running these.

## C++ Interface <a id='c-interface'></a>

If you want to build nvblox into a larger project, without ROS, or you would like to make modifications to nvblox's core reconstruction features, this repository contains the code you need. Our [tutorial](docs/pages/tutorial_library_interface.md) provides some brief details of how to interact with the reconstruction in c++.


# Native Installation <a id='native-installation'></a>
If you want to build natively, please follow these instructions. Instructions for docker are [further below](#docker).

## Install dependencies <a id='install-dependencies'></a>
We depend on:
- gtest
- glog
- gflags
- SQLite 3
- CUDA 11.0 - 12.2 (others might work but are untested)
- Eigen (no need to explicitly install, a recent version is built into the library)
- stdgpu (downloaded during compilation)
Please run
```
sudo apt-get install -y libgoogle-glog-dev libgtest-dev libgflags-dev python3-dev libsqlite3-dev libbenchmark-dev
cd /usr/src/googletest && sudo cmake . && sudo cmake --build . --target install
```

## Build and run tests and benchmark <a id='build-and-run-tests-and-benchmark'></a>
Build:
```
cd nvblox/nvblox
mkdir build
cd build
cmake .. && make
```

Run test and benchmark from build dir:
```
ctest
```


## Run an example <a id='run-an-example'></a>
In this example we fuse data from the [3DMatch dataset](https://3dmatch.cs.princeton.edu/). First let's grab the dataset. Here I'm downloading it to my dataset folder `~/datasets/3dmatch`.
```
wget http://vision.princeton.edu/projects/2016/3DMatch/downloads/rgbd-datasets/sun3d-mit_76_studyroom-76-1studyroom2.zip -P ~/datasets/3dmatch
unzip ~/datasets/3dmatch/sun3d-mit_76_studyroom-76-1studyroom2.zip -d ~/datasets/3dmatch
```
Navigate to and run the `fuse_3dmatch` binary. From the nvblox base folder run
```
cd nvblox/build/executables
./fuse_3dmatch ~/datasets/3dmatch/sun3d-mit_76_studyroom-76-1studyroom2/ mesh.ply
```
Once it's done we can view the output mesh using the Open3D viewer. Instructions for installing open3d-viewer can be found below.
```
Open3D mesh.ply
```
You should see a mesh of a room:
![](docs/images/reconstruction_in_docker_trim.png)


# Docker <a id='docker'></a>

We have several dockerfiles (in the `docker` subfolder) which layer on top of one another for the following purposes:

* **Docker.deps**
  * This installs our dependencies.
* **Docker.jetson_deps**
  * Same as above, just on the Jetson (Jetpack 6 and above).
* **Docker.build**
  * Layers on top of Docker.deps.
  * This builds our package.

We rely on nvidia docker. Install the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) following the instructions on that website.

We use the GPU during build, not only at run time. In the default configuration the GPU is only used at at runtime. One must therefore set the default runtime. Add `"default-runtime": "nvidia"` to `/etc/docker/daemon.json` such that it looks like:
```
{
    "runtimes": {
        "nvidia": {
            "path": "/usr/bin/nvidia-container-runtime",
            "runtimeArgs": []
         }
    },
    "default-runtime": "nvidia"
}
```
Restart docker
```
sudo systemctl restart docker
```
Now Let's build Dockerfile.deps docker image. This image install contains our dependencies.
```
docker build -t nvblox_deps -f docker/Dockerfile.deps .
```
> In case you are running this on the Jetson, substitute the dockerfile: `docker/Dockerfile.jetson_deps`

Now let's build the Dockerfile.build. This image layers on the last, and actually builds the nvblox library.
```
docker build -t nvblox -f docker/Dockerfile.build .
```
Now let's run the 3DMatch example inside the docker. Note there's some additional complexity in the `docker run` command such that we can forward X11 to the host (we're going to be view a reconstruction in a GUI). Note that visualization does not work over SSH connections. Run the container using:
```
xhost local:docker
docker run -it --net=host --env="DISPLAY" -v $HOME/.Xauthority:/root/.Xauthority:rw -v /tmp/.X11-unix:/tmp/.X11-unix:rw nvblox
```
Let's download a dataset and run the example (this is largely a repeat of "Run an example" above).
```
apt-get update
apt-get install unzip
wget http://vision.princeton.edu/projects/2016/3DMatch/downloads/rgbd-datasets/sun3d-mit_76_studyroom-76-1studyroom2.zip -P ~/datasets/3dmatch
unzip ~/datasets/3dmatch/sun3d-mit_76_studyroom-76-1studyroom2.zip -d ~/datasets/3dmatch
cd nvblox/nvblox/build/executables/
./fuse_3dmatch ~/datasets/3dmatch/sun3d-mit_76_studyroom-76-1studyroom2/ mesh.ply
```
Now let's visualize. From the same executable folder run:
```
apt-get install libgl1-mesa-glx libc++1 libc++1-10 libc++abi1-10 libglfw3 libpng16-16
wget https://github.com/isl-org/Open3D/releases/download/v0.13.0/open3d-app-0.13.0-Ubuntu_20.04.deb
dpkg -i open3d-app-0.13.0-Ubuntu_20.04.deb
Open3D mesh.ply
```
to visualize on the jetson see [below](#open3d-on-jetson).

# Open3D on Jetson <a id='open3d-on-jetson'></a>

Open3D is available pre-compiled for the jetson ([details here](http://www.open3d.org/docs/release/arm.html)). Install via pip:
```
sudo apt-get install python3-pip
sudo pip3 install open3d==0.16.0
```
> If version `0.16.0` is not available you need to upgrade your pip with `pip3 install -U pip`. You may additionally need to add the upgraded pip version to your path.

View the mesh via:
```
open3d draw mesh.ply
```

# Building for multiple GPU architectures <a id='building-for-multiple-gpu-architectures'></a>
By default, the library builds ONLY for the compute capability (CC) of the machine it's being built on. To build binaries that can be used across multiple machines (i.e., pre-built binaries for CI, for example), you can use the `CMAKE_CUDA_ARCHITECTURE` flag and set it to a semicolon-separated list of architectures to support.
```
cmake .. '-DCMAKE_CUDA_ARCHITECTURES=75;72' -DCMAKE_INSTALL_PREFIX=../install/ && make -j8 && make install
```

# Building redistributable binaries, with static dependencies <a id='building-redistributable-binaries-with-static-dependencies'></a>
If you want to include nvblox in another CMake project, simply `find_package(nvblox)` should bring in the correct libraries and headers. However, if you want to include it in a different build system such as Bazel, you can see the instructions [here](./docs/redistributable.md).

# License <a id='license'></a>
This code is under an [open-source license](@ref license) (Apache 2.0). :)

# Paper <a id='paper'></a>
If you find this library useful for your research, please consider citing our paper:

* Alexander Millane, Helen Oleynikova, Emilie Wirbel, Remo Steiner, Vikram Ramasamy, David Tingdahl, and Roland Siegwart. "**nvblox: GPU-Accelerated Incremental Signed Distance Field Mapping**".
arXiv preprint arXiv:2311.00626. \[ [ArXiv](https://arxiv.org/abs/2311.00626) \]

```bibtex
@misc{millane2024nvblox,
      title={nvblox: GPU-Accelerated Incremental Signed Distance Field Mapping},
      author={Alexander Millane and Helen Oleynikova and Emilie Wirbel and Remo Steiner and Vikram Ramasamy and David Tingdahl and Roland Siegwart},
      year={2024},
      eprint={2311.00626},
      archivePrefix={arXiv},
      primaryClass={cs.RO}
}
```
