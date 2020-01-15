from keras.models import load_model
from skimage import io, measure, feature, morphology
import numpy as np


def count_cells(input_img, sigma=4):
    absolute_output = np.abs(input_img)
    canny_output = feature.canny(absolute_output, sigma=sigma)
    closed_output = morphology.binary_closing(canny_output, selem=np.ones((3,3)))
    labeled_output = measure.label(canny_output)
    count = len(np.unique(labeled_output)) - 1
    return count


def count_nuclei(pred_img): 
    pred_img = (pred_img>0.3).astype(np.uint8) 
    pred_img_eroded = morphology.binary_erosion(pred_img, np.ones((5,5))) 
    pred_label = measure.label(pred_img_eroded) 
    count = 0 
    for label in np.unique(pred_label): 
     if np.sum((pred_label==label).astype(np.uint8)) >= 10: 
         count += 1 
    return count


def get_count_for_one_image(path_to_img):
    model = load_model("../../../models/cell_counting_model_v_2.hdf5")
    img = io.imread(path_to_img)
    y_pred = model.predict( np.asarray([img]))[0]
    test_cell_count = count_cells(y_pred[:,:,0])
    print("="*40, "\n{} Cells are detected !".format(test_cell_count))
    return test_cell_count


get_count_for_one_image("../../../data/cervix_images/frame050_stack_fov000_0.png")