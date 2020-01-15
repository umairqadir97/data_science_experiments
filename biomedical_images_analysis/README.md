Pathware-Biopsy/Cytology
==============================

Using computer vision to better understand biposy/cytology microscope slides

[Project Documentation](https://docs.google.com/document/d/1mdC-tELAEqthM6j2QrP-rhx-mH6cpWc1gR2xkbnvVZE/edit?usp=sharing)

[Dataset](https://github.com/parham-ap/cytology_dataset)

Project Organization
------------

    ├── LICENSE
    ├── README.md                       <- The top-level README for developers using this project.
    ├── data
    │   ├── cervix_miages               <- Final Dataset Images gereatred by script in src/prepare_cervix_data.py
    │   └── cervix_labels               <- Final Dataset Labels gereatred by script in src/prepare_cervix_data.py
    │   └── cervix_nuclei_count         <- Cell's coutn Ground truth for all image samples
    │   └── cervix_93_cytology_dataset  <- Original Cytology Dataset
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks for experimentation.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    |
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── prepare_cervix_data.py
    │   │
    |   |
    │   ├── cell_counting_experimentation    <- Counting cell with ConvNet based regression model
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
    |   |
    │   │
    │   ├── models         <- Saved model files
    |   |
