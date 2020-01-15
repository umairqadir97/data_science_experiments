import os
import random

image_folder = "../../data/cervix_images"

image_names = os.listdir(image_folder)
image_names = [img_name.replace(".jpg", "") for img_name in image_names]

random.shuffle(image_names)

train_images_names = image_names[:7375]
val_images_names = image_names[7375:8425]
test_images_names = image_names[8425:]

with open('train.txt', mode='wt', encoding='utf-8') as myfile:
    myfile.write('\n'.join(train_images_names))
with open('val.txt', mode='wt', encoding='utf-8') as myfile:
    myfile.write('\n'.join(val_images_names))
with open('trainval.txt', mode='wt', encoding='utf-8') as myfile:
    myfile.write('\n'.join(train_images_names+val_images_names))
with open('test.txt', mode='wt', encoding='utf-8') as myfile:
    myfile.write('\n'.join(test_images_names))
