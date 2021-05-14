# Falling-Person-Detection-based-On-AlphaPose
A PyTorch implementation for Falling person detection inside elevator based on AlphaPose Estimation (Human body keypoints detection)

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

* [Falling-Person-Detection-based-On-AlphaPose](#Falling-Person-Detection-based-On-AlphaPose)
	* [Requirements](#requirements)
	* [Features](#features)
	* [Folder Structure](#folder-structure)
	* [Usage](#usage)
		* [Config file format](#config-file-format)
    * [Using Multiple GPU](#using-multiple-gpu)
	* [Customization](#customization)
		* [Custom CLI options](#custom-cli-options)
		* [Data Loader](#data-loader)
		* [Trainer](#trainer)
		* [Model](#model)
		* [Loss](#loss)
		* [metrics](#metrics)
		* [Additional logging](#additional-logging)
		* [Validation data](#validation-data)
		* [Checkpoints](#checkpoints)
    * [Tensorboard Visualization](#tensorboard-visualization)
	* [Contribution](#contribution)
	* [TODOs](#todos)
	* [License](#license)
	* [Acknowledgements](#acknowledgements)

<!-- /code_chunk_output -->


## Features
* Clear folder structure which is suitable for many deep learning projects.
* `.json` config file support for convenient parameter tuning.
* Customizable command line options for more convenient parameter tuning.
* Checkpoint saving and resuming.

## Folder Structure
  ```
  Falling-Person-Detection-based-On-AlphaPose/
  │
  ├── train/ contains training scripts for dnn and RNNS fall classification models
  |    ├──  train_dnn.py - script to start dnn training
  |    ├──  train_ae.py - script to start auto encoder training
  |    ├──  train_aelstm.py - script to start auto encode plus lstm training
  |    ├──  train_lstm.py - script to start lstm training
  |    ├──  dataloader.py - skeleton dataloader
  |    ├──  plot_statics.py - plot training stats 
  |
  ├── test/ contains  scripts to inference trained models on videos and image data
  |    ├── main.py - main script to run inference on video data
  |
  ├── source/contains alphapose source code  
  |    ├── check alphapose source readme for getting started
  |    ├── check alaphapose docs folder for installation 
  │
  │
  ├── dataset/  - contains skeleton data extracted from alphapose estimator 
  │   └── DataCSV
  |    └── DataPrepare 
  |    └── SkeletonData
  │
  ├── input/ - default directory for storing image and video datasets
  |	└── multicam_dataset - these are used as input to pose estimator for extracting skeleton data
  |	└── Falling_Standing
  |	└── Falling_Standing_2
  │
  ├── examples - contains test video for inferece 
  |
  ├── fallmodels/ - fall classification models package
  │   ├── model.py
  │     
  │
  ├── checkpoints/ fall classification models checkpoints
  │   ├── dnntiny/ - trained models are saved here
  |          ├── epoch_210_loss_0.031925.pth
  │
  ├── plots/ - module for tensorboard visualization and logging
  │   
  │  
  └── tools/ - small utility functions
      ├── cut_frames.py
      └── video2images.py
  ```
## Requirements
* Python >= 3.5 (3.7 recommended)
* PyTorch >= 0.4 (1.2 recommended)
* See alphapose [readme](https://github.com/rashidch/Falling-Person-Detection-based-On-AlphaPose/tree/main/source) 
	and [installation docs](https://github.com/rashidch/Falling-Person-Detection-based-On-AlphaPose/blob/main/source/docs/INSTALL.md) for complete requirements
* After complete installation including Alphapose cd to root directory (Falling-Person-Detection-based-On-AlphaPos) and follow commands in usage section to extract sekelton data, run train and inference on videos
	
## Usage

* Extract skeleton data:
  ```
  python dataset/dataPrepare/get_keypoints.py --cfg source/configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml --checkpoint source/pretrained_models/fast_res50_256x192.pth --indir input/Falling_Standing_2 --outdir frames --save_img --qsize 50
  ```
* Train fall classification models
  ```
  python train/train_dnn.py
  ```
* Run on trained fall models
  ```
  python test/main.py --cfg source/configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml --checkpoint source/pretrained_models/fast_res50_256x192.pth --cam examples/demo/test/1.mp4 --vis_fast --save_out outputs/1.avi
  ```
* Check [alphapose docs](https://github.com/rashidch/Falling-Person-Detection-based-On-AlphaPose/blob/main/source/docs/run.md) for explanation of command line arguments 

### Config file format
* [Alphapose Config files ](https://github.com/rashidch/Falling-Person-Detection-based-On-AlphaPose/blob/main/source/configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml)
* [Fall classfication models Config files ](https://github.com/rashidch/Falling-Person-Detection-based-On-AlphaPose/tree/main/test/classifier_config)
* Add addional configurations if you need.



## Contribution
Feel free to contribute any kind of function or enhancement, here the coding style follows PEP8

Code should pass the [Flake8](http://flake8.pycqa.org/en/latest/) check before committing.

## TODOs

- [ ] Multiple optimizers
- [ ] Support more tensorboard functions
- [x] Using fixed random seed
- [x] Support pytorch native tensorboard
- [x] `tensorboardX` logger support
- [x] Configurable logging layout, checkpoint naming
- [x] Iteration-based training (instead of epoch-based)
- [x] Adding command line option for fine-tuning

## License
This project is licensed under the MIT License. See  LICENSE for more details

## Acknowledgements
This project is inspired by the project [Tensorflow-Project-Template](https://github.com/MrGemy95/Tensorflow-Project-Template) by [Mahmoud Gemy](https://github.com/MrGemy95)

