import os
import csv
import zipfile
import numpy as np
from collections import defaultdict
from skimage import io, draw, measure, transform
from google_drive_downloader import GoogleDriveDownloader as gdd

dataset_path = "../data/cervix93_cytology_dataset"
image_shape = (224, 224)

# def show(img):
#     io.imshow(img)
#     io.show()

def resize_fix(img, shape=(224,224)):
    resized_img = transform.resize(img, shape).astype(np.bool)
    # show(resized_img)
    resized_img = (resized_img).astype(np.uint8)
    # show(resized_img)
    return resized_img


def download_data(dataset_path):
    """Checks if data exists, otherwise downloads and unzips"""
    if not os.path.isdir(dataset_path):
        if not os.path.isfile(dataset_path+".zip"):
            gdd.download_file_from_google_drive(file_id="1h47eAEi5aSvEftetsy-fQmhqSG1lhvWP",
                                                dest_path=dataset_path+".zip")
        with zipfile.ZipFile(dataset_path+".zip", "r") as zip_ref:
            zip_ref.extractall(dataset_path)


def create_mask_and_augment(label_to_imgs):
    """
    Read nuclei coordinates from csv file and create label images.
    Afterwards it augments data by dividing the image into its 4 quarters
    It also resizes the images to 256*256 and saves them
    """
    for label_path in label_to_imgs:
        imgs = label_to_imgs[label_path]

        coords = []
        with open(label_path, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                coords.append(row)

        first_img = io.imread(imgs[0])

        label_img = np.zeros((first_img.shape[0], first_img.shape[1]))#, dtype=np.float16)

        for coord in coords:
            try:
                rr, cc = draw.circle(int(coord[0]), int(coord[1]), 15)
                label_img[rr, cc] = 1
            except IndexError:
                pass

        label_img_quar1 = label_img[:int(first_img.shape[0] / 2), :int(first_img.shape[1] / 2)]
        label_img_quar1 = resize_fix(label_img_quar1)

        label_img_quar2 = label_img[:int(first_img.shape[0] / 2), int(first_img.shape[1] / 2):]
        label_img_quar2 = resize_fix(label_img_quar2)

        label_img_quar3 = label_img[int(first_img.shape[0] / 2):, :int(first_img.shape[1] / 2)]
        label_img_quar3 = resize_fix(label_img_quar3)

        label_img_quar4 = label_img[int(first_img.shape[0] / 2):, int(first_img.shape[1] / 2):]
        label_img_quar4 = resize_fix(label_img_quar4)

        label_img = resize_fix(label_img)

        for img_path in imgs:
            if "stack" in img_path:
                filename = "_".join(img_path.split("/")[-2:]).replace(".png", "")
            else:
                filename = img_path.split("/")[-1].replace(".png", "")

            img = io.imread(img_path)
            img = np.dstack((img, img, img))

            img_quar1 = img[:int(img.shape[0] / 2), :int(img.shape[1] / 2)]
            img_quar1 = (transform.resize(img_quar1, (224, 224)) * 255).astype(np.uint8)

            img_quar2 = img[:int(img.shape[0] / 2), int(img.shape[1] / 2):]
            img_quar2 = (transform.resize(img_quar2, (224, 224)) * 255).astype(np.uint8)

            img_quar3 = img[int(img.shape[0] / 2):, :int(img.shape[1] / 2)]
            img_quar3 = (transform.resize(img_quar3, (224, 224)) * 255).astype(np.uint8)

            img_quar4 = img[int(img.shape[0] / 2):, int(img.shape[1] / 2):]
            img_quar4 = (transform.resize(img_quar4, (224, 224)) * 255).astype(np.uint8)

            img = (transform.resize(img, (224, 224)) * 255).astype(np.uint8)

            io.imsave(os.path.join("../data/cervix_images", filename+"_0.png"), img)
            io.imsave(os.path.join("../data/cervix_images", filename + "_1.png"), img_quar1)
            io.imsave(os.path.join("../data/cervix_images", filename + "_2.png"), img_quar2)
            io.imsave(os.path.join("../data/cervix_images", filename + "_3.png"), img_quar3)
            io.imsave(os.path.join("../data/cervix_images", filename + "_4.png"), img_quar4)

            io.imsave(os.path.join("../data/cervix_labels", filename + "_0.png"), label_img)
            io.imsave(os.path.join("../data/cervix_labels", filename + "_1.png"), label_img_quar1)
            io.imsave(os.path.join("../data/cervix_labels", filename + "_2.png"), label_img_quar2)
            io.imsave(os.path.join("../data/cervix_labels", filename + "_3.png"), label_img_quar3)
            io.imsave(os.path.join("../data/cervix_labels", filename + "_4.png"), label_img_quar4)

            with open(os.path.join("../data/cervix_nuclei_count", filename+"_0.txt"), "w") as out:
                out.write(str(len(coords)))
            with open(os.path.join("../data/cervix_nuclei_count", filename+"_1.txt"), "w") as out:
                out.write(str(len(np.unique(measure.label(label_img_quar1)))-1))
            with open(os.path.join("../data/cervix_nuclei_count", filename+"_2.txt"), "w") as out:
                out.write(str(len(np.unique(measure.label(label_img_quar2)))-1))
            with open(os.path.join("../data/cervix_nuclei_count", filename+"_3.txt"), "w") as out:
                out.write(str(len(np.unique(measure.label(label_img_quar3)))-1))
            with open(os.path.join("../data/cervix_nuclei_count", filename+"_4.txt"), "w") as out:
                out.write(str(len(np.unique(measure.label(label_img_quar4)))-1))


download_data(dataset_path)

### The following code is specific to cervix image dataset ###
all_clear_image_names = os.listdir(dataset_path+"/EDF")
all_clear_image_names  = [clear_image for clear_image in all_clear_image_names if clear_image[-4:] == ".png"]
all_clear_image_names = [os.path.join(dataset_path, "EDF", clear_image) for clear_image in all_clear_image_names]
all_image_label_names = [image_name.replace(".png", ".csv") for image_name in all_clear_image_names]

all_folders = os.listdir(dataset_path)
all_blur_folders = [folder for folder in all_folders if folder[:5] == "frame"]
all_blur_folders = [os.path.join(dataset_path, folder) for folder in all_blur_folders]

all_blur_image_names = []
for blur_folder in all_blur_folders:
    blur_image_names = os.listdir(blur_folder)
    blur_image_names = [os.path.join(blur_folder, image_name) for image_name in blur_image_names]
    all_blur_image_names += blur_image_names

label_to_imgs = defaultdict(lambda:[])
for label_path in all_image_label_names:
    label_to_imgs[label_path] += [img_name for img_name in all_clear_image_names if img_name[-7:-4] == label_path[-7:-4]]
    label_to_imgs[label_path] += [img_name for img_name in all_blur_image_names if img_name[-20:-17] == label_path[-7:-4]]

if not os.path.isdir("../data/cervix_images"):
    os.mkdir("../data/cervix_images")
if not os.path.isdir("../data/cervix_labels"):
    os.mkdir("../data/cervix_labels")
if not os.path.isdir("../data/cervix_nuclei_count"):
    os.mkdir("../data/cervix_nuclei_count")

create_mask_and_augment(label_to_imgs)
