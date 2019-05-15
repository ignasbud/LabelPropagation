# LabelPropagation

This project provides the implementation of label propagation of Budvytis et. al, **Large scale labelled video data augmentation for semantic segmentation in driving scenarios.** *In ICCV Workshop track, Venice, October 2017* [1]

[paper](http://mi.eng.cam.ac.uk/~cipolla/publications/inproceedings/2017-ICCV-label-propagation.pdf)
<!--- [supplementary]()--->

 <!---[![Label propagation in CityScapes dataset](web/cityscapes_class_propagation.gif)](https://www.youtube.com/watch?v=mF5PTV1S9_Q")--->
  
 <!--[![Class label propagation in CityScapes Dataset](web/cityscapes_class_propagation.gif)](https://www.youtube.com/watch?v=mF5PTV1S9_Q)-->
 
<!--[![Class label propagation in CityScapes Dataset](http://mi.eng.cam.ac.uk/~ib255/files/external/cityscapes_class_propagation_15_20.gif)](https://www.youtube.com/watch?v=mF5PTV1S9_Q)-->

 <img src="http://mi.eng.cam.ac.uk/~ib255/files/external/cityscapes_class_propagation_15_20.gif" data-canonical-src="http://mi.eng.cam.ac.uk/~ib255/files/external/cityscapes_class_propagation_15_20.gif" width="100%" />
 
 <img src="http://mi.eng.cam.ac.uk/~ib255/files/external/cityscapes_instance_propagation.gif" data-canonical-src="http://mi.eng.cam.ac.uk/~ib255/files/external/cityscapes_instance_propagation.gif" width="100%" />
 
<!--[![Instance label propagation in CityScapes Dataset](http://mi.eng.cam.ac.uk/~ib255/files/external/cityscapes_instance_propagation.gif)](https://www.youtube.com/watch?v=mF5PTV1S9_Q)-->

<!---[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/mF5PTV1S9_Q/0.jpg)](https://www.youtube.com/watch?v=mF5PTV1S9_Q)--->

## Getting Started

Instructions below explain prerequisites and installation steps needed.

### Prerequisites

- Python2.7
- numpy
- OpenCV3.4.1

### Compatible GPU setups

GPU code compiled with:

```
- {"gpu":"GeForce GTX 1080", "cuda":"8.0",  "driver":"370.28"}
```

GPU code tested with:
```
- {"gpu":"Tesla V100-SXM2-16GB", "cuda":"10.1",  "driver":"418.40.04"},
- {"gpu":"GeForce GTX 1080", "cuda":"8.0",  "driver":"370.28"},
- {"gpu":TITAN X (Pascal)","cuda":"10.0","driver":"410.104"},
- {"gpu":TITAN Xp","cuda":"10.0","driver":"410.104"}
```
See [bin/compilation_info.json](bin/compilation_info.json) for more up-to-date detail.

<!--- ### Installing
A step by step series of examples that tell you how to get a development env running
```
Give the example
```
And repeat
```
until finished
```
End with an example of getting some data out of the system or using it for a little demo
--->

## Running the code

### Step-1 creating binary images

```
python ./scripts/experiment_create_binary_images.py ./configs/config_camvid360.json
```
Script executed by **create_binary_images.sh** takes a folder with png images (e.g. ./data/camvid360/images/) and creates a project folder (e.g. ```./sample_outputs/camvid360/```), within which it creates raw binary copies of the images read (e.g. ```./sample_outputs/camvid360/binary_images/```). All data directory and algorithm information is stored in config file (e.g. ```./configs/config_camvid360.json```)


### Step-2 creating frame to frame mappings

```
python ./scripts/experiment_calculate_mappings.py ./configs/config_camvid360.json 0
```
Script executed by **calculate_mappings.sh** takes a folder with binary images (e.g. ```./sample_outputs/camvid360/```) and calculate forward ("O") and backward ("OR") mappings between neighbouring images. The mappings are stored in a special project folder (e.g. ```./sample_outputs/camvid360/mappings/```). GPU ID (e.g. ```0```) is also passed in order to execute the code on a desired gpu.


### Step-3 performing label propagation

```
python ./scripts/experiment_launch_propagation.py ./configs/config_camvid360.json 0 ./sample_outputs/camvid360/images_binary/R0010094_20170622125256_er_f_00008010.bin
```

Script executed by **perform_propagation.sh** takes a seed image name (e.g. ```./sample_outputs/camvid360/images_binary/R0010094_20170622125256_er_f_00008010.bin```) from which to perform a propagation. GPU ID (e.g. ```0```) is also passed in order to execute the code on a desired gpu. Config file (e.g. ```./configs/config_camvid360.json```) stores the "half_propagation_distance" parameter in order to determine the length of the label propagation.

## GPU code

Note that code responsible for actual calculation of correspondences between images and label propagation is pre-compiled with certain parameters for reasons of efficiency and legacy. Some of those parameters are explained below. Also note that currently only pre-compiled binaries are provided (see ```./bin/mappings/``` or ```./bin/propagation/```)

### Calculating correspondences between images

File names (e.g. ```bin/mappings/mappings_v40_GROUP_01_WH_1024x1024_wind_255x255_HP_3```) of code performing image correspondence calculation encode the following information:

- code version (e.g. ```v40```)
- compilation type/group (e.g. ```GROUP_01```)
- maximum image dimensions for width and height (e.g. ```WH_1024x1024```)
- maximum sliding window image dimensions centered around a pixel of interest for width and height (e.g. ```wind_255x255```)

### Propagating labels

File names (e.g. ```bin/propagation/propagation_gpu_v9_GROUP_01_maxclass_31```) of code performing label propagation encode the following information:

- code version (e.g. ```v9```)
- compilation type/group (e.g. ```GROUP_01```)
- maximum number of classes per partial propagation (e.g. ```maxclass_31```)

## Comments on reproducability of [1]

This code is a close, but not an identical replica of the code used in [1]. Explanations of the differences may be added in the future.

## TO-DO List

- Add a more detailed explation of different parts of the algorithms.
- Add the c++ code of image mapping and label propagation instead of binaries.
- [TBD]

## Citations

If you use this code please cite the following publications:

```
@InProceedings{Budvytis2017ICCV,
               author = {Budvytis, I. and Sauer, P. and Roddick, T. and Breen, K. and Cipolla, R.},
               title = {Large Scale Labelled Video Data Augmentation for Semantic Segmentation in Driving Scenarios},
               booktitle = {5th Workshop on Computer Vision for Road Scene Understanding and Autonomous Driving in IEEE International Conference on Computer Vision (ICCV)},
               month = {October},
               year = {2017}
}

@article{BadrinarayananBC13,
               author    = {Vijay Badrinarayanan and Ignas Budvytis and Roberto Cipolla},
               title     = {Semi-Supervised Video Segmentation Using Tree Structured Graphical Models},
               journal   = {{IEEE} Transactions on Pattern Analysis and Machine Intelligence},
               volume    = {35},
               number    = {11},
               pages     = {2751--2764},
               year      = {2013}  
}
```

## References

[1] Budvytis, I., Sauer, P., Roddick, T., Breen, K., Cipolla, R., 
**Large scale labelled video data augmentation for semantic segmentation in driving scenarios.** *In 5th Workshop on Computer Vision for Road Scene Understanding and Autonomous Driving in IEEE International Conference on Computer Vision (ICCV), Venice, October 2017* 
