# LabelPropagation

This project provides the implementation of label propagation of Budvytis et. al, **Large scale labelled video data augmentation for semantic segmentation in driving scenarios.** *In ICCV Workshop track, Venice, October 2017* [1]

[paper](http://mi.eng.cam.ac.uk/~cipolla/publications/inproceedings/2017-ICCV-label-propagation.pdf)
<!--- [supplementary]()--->

 <!---[![Label propagation in CityScapes dataset](web/cityscapes_class_propagation.gif)](https://www.youtube.com/watch?v=mF5PTV1S9_Q")--->
  
 <!--[![Class label propagation in CityScapes Dataset](web/cityscapes_class_propagation.gif)](https://www.youtube.com/watch?v=mF5PTV1S9_Q)-->
 
[![Class label propagation in CityScapes Dataset](http://mi.eng.cam.ac.uk/~ib255/files/external/cityscapes_class_propagation_15_20.gif)](https://www.youtube.com/watch?v=mF5PTV1S9_Q)
 <img src="http://mi.eng.cam.ac.uk/~ib255/files/external/cityscapes_class_propagation_15_20.gif" data-canonical-src="http://mi.eng.cam.ac.uk/~ib255/files/external/cityscapes_class_propagation_15_20.gif" width="200" height="400" />
 
[![Instance label propagation in CityScapes Dataset](http://mi.eng.cam.ac.uk/~ib255/files/external/cityscapes_instance_propagation.gif)](https://www.youtube.com/watch?v=mF5PTV1S9_Q)

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

Explain how to run the automated tests for this system

## References

[1] Budvytis, I., Sauer, P., Roddick, T., Breen, K., Cipolla, R., 
**Large scale labelled video data augmentation for semantic segmentation in driving scenarios.** *In 5th Workshop on Computer Vision for Road Scene Understanding and Autonomous Driving in IEEE International Conference on Computer Vision (ICCV), Venice, October 2017* 
