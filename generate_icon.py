#!/usr/bin/env python3
import cv2
import numpy as np
import os


def display(img):
    cv2.imshow('prout', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def crop(img):
    channels = cv2.split(img)
    alpha = channels[3]
    _, thresh = cv2.threshold(alpha, 127, 255, 0)
    _,contours, _ = cv2.findContours(thresh, 1, 2)
    cnt = contours[-1]
    xmin, ymin, width, height = cv2.boundingRect(cnt)
    dim = max(width, height)
    #return img[ymin:ymin+height, xmin:xmin+width]
    return img[ymin:ymin+dim, xmin:xmin+dim]


def blur(img):
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    return blur


def resize(img):
    res = cv2.resize(img, (30, 30), interpolation=cv2.INTER_LINEAR)
    return res


def fit_to_size(img, size):
    vertical_missing = size[0] - img.shape[0]
    horizontal_missing = size[1] - img.shape[1]
    top_border = vertical_missing//2
    if vertical_missing%2 == 0:
        bottom_border = vertical_missing//2
    else:
        bottom_border = vertical_missing//2 + 1
    left_border = horizontal_missing//2
    if horizontal_missing%2 == 0:
        right_border = horizontal_missing//2
    else:
        right_border = horizontal_missing//2 + 1

    border = cv2.copyMakeBorder(img, top=top_border, bottom=bottom_border,
                                left=left_border, right=right_border,
                                borderType=cv2.BORDER_CONSTANT,
                                value=[0, 0, 0, 0])
    return border


def outline(img):
    channels = cv2.split(img)
    alpha = channels[3]
    edges = cv2.Canny(alpha, 100, 200)
    outline = np.argwhere(edges > 0)
    for i, j in outline:
        img[i, j] = (0, 0, 0, 255)
    return img


def main():
    for i in range(252, 387):
        filename = 'original-icons/{}.png'.format(i)
        try:
            original = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
            larger = crop(original)
            if larger.shape[0] > 93 or larger.shape[1] > 93:
                max_dim = max(larger.shape[0], larger.shape[1])
                ratio = 93/max_dim
                dim = (int(ratio*larger.shape[1]), int(ratio*larger.shape[0]))
                larger = cv2.resize(larger, dim, cv2.INTER_LINEAR)
            larger = outline(larger)
            #larger = blur(larger)
            larger = fit_to_size(larger, (93, 93))

            if larger.shape[0] > 30 or larger.shape[1] > 30:
                max_dim = max(larger.shape[0], larger.shape[1])
                ratio = 30/max_dim
                dim = (int(ratio*larger.shape[1]), int(ratio*larger.shape[0]))
                icon = cv2.resize(larger, dim, cv2.INTER_LINEAR)
            icon = outline(icon)
            icon = fit_to_size(icon, (30, 30))

            cv2.imwrite('icons/{}.png'.format(i), icon)
            cv2.imwrite('larger-icons/{}.png'.format(i), larger)
        except Exception as e:
            print('Something bad happened with {}.png'.format(i))
            print(e)


if __name__ == '__main__':
    main()

