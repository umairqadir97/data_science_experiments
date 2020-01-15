from skimage import io, draw, color
import numpy as np
import argparse
import json
import os

def show(img):
    io.imshow(img)
    io.show()

def overlay_on_gray(oimg ,overlayGREEN=None ,overlayRED=None ,overlayBLUE=None ,alpha = 0.6):
    rows, cols = oimg.shape
    color_mask = np.zeros((rows, cols, 3))
    if overlayGREEN is not None:
        color_mask[: ,: ,1] = overlayGREEN
    if overlayRED  is not None:
        color_mask[: ,: ,2] = overlayRED
    if overlayBLUE is not None:
        color_mask[: ,: ,0] = overlayBLUE

    img_color = np.dstack((oimg, oimg, oimg))

    img_hsv = color.rgb2hsv(img_color)
    color_mask_hsv = color.rgb2hsv(color_mask)

    img_hsv[..., 0] = color_mask_hsv[..., 0]
    img_hsv[..., 1] = color_mask_hsv[..., 1] * alpha
    img_masked = color.hsv2rgb(img_hsv)

    return img_masked ,color_mask


def get_mask_from_polygons(polygons, shape=None):
    mask_tissue = np.zeros(shape=(shape[0], shape[1]), dtype=np.uint8)
    mask_artifact = np.zeros(shape=(shape[0], shape[1]), dtype=np.uint8)
    for polygon in polygons:
        label = polygon['label']
        poly_points = np.array(polygon['points']).T
        c, r = poly_points[0], poly_points[1]
        rr,cc = draw.polygon(r,c)
        if label == 'tissue':
            mask_tissue[rr,cc] = 255
        else:
            mask_artifact[rr,cc] = 255
    return mask_tissue, mask_artifact


if __name__=='__main__':

    # RED IS TISSUE
    # BLUE IS ARTIFACT

    parser = argparse.ArgumentParser(description='Add overlays')
    parser.add_argument("--input_img", help="Input Image")
    parser.add_argument("--input_label", help="Input Label")
    args = parser.parse_args()

    img = io.imread(args.input_img)
    polygons = json.load(open(args.input_label))
    mask_tissue, mask_artifact = get_mask_from_polygons(polygons['shapes'], shape=img.shape)

    output_overlay_img, _ = overlay_on_gray(img, overlayBLUE=mask_tissue, overlayRED=mask_artifact)
    io.imsave(os.path.join(args.input_img), (output_overlay_img * 255).astype(np.uint8))

