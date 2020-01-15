Pathware-Biopsy/Cytology
==============================

Using different computer vision techniquesto count cell in biposy/cytology microscopic slide images

Module Organization
------------

    src──
    │   |── cell_counting_experimentation    <- Counting cell with ConvNet based regression model
    │   │   ├── v1_cell_counting
    |   |       └── cell_counting_ConvNet.py
    |   |
    |   |
    |   |   ├──v2_cell_counting              <- Training a U-Net model for nuclei segmentation and then counting
    |   |       |── generator.py
    |   |       |── model.py
    |   |       |── train.py
    |   |       |── test.py
    |   |       |── iou_evaluation.py
    |   |


Cell Counting
------------

## V1_Cell_Counting_ConvNet
- An approach to solve cell counting problem with regression on images through Convolutional Neural Network
- Dataset: Cytology Cells Data

##### Performance
- Model was not perofrming good, count was far away from ground truth


## V2_Cell_Counting_U-Net
- This approach used U-Net model for nuclei segmentation
- Count was then calculated by applying some threshold and other DIP functions on predicted segmented image

##### Performance
- Due to post processing the images to get count of cells, results were varying. But still acceptable
- IOU score for segmentation with threshold 0.3 = 0.557
- 