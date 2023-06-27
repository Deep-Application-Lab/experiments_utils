#!/usr/bin/env python
# !-*-coding:utf-8 -*-
# !@Time    :2023/6/26 16:18
# !@Author  : murInj
# !@Filer    : .py
import os
import shutil
from typing import List
from general.io_utils import create_directory, clear_directory, tail_directory_func
from general.json_utils import write_json
import cv2


def LSC(img,
        iterate: int = 10,
        label: bool = False,
        number: bool = False,
        mask: bool = False,
        on_img: bool = True):
    lsc = cv2.ximgproc.createSuperpixelLSC(img)
    lsc.iterate(iterate)  # 迭代次数越大，效果越好
    if not label and not number and not mask and not on_img:
        return lsc
    results = dict()
    if label:
        results['label'] = lsc.getLabels()
    if mask:
        results['mask'] = lsc.getLabelContourMask()
    if number:
        results['number'] = lsc.getNumberOfSuperpixels()
    if on_img:
        mask_inv_lsc = cv2.bitwise_not(lsc.getLabelContourMask())
        results['on_img'] = cv2.bitwise_and(img, img, mask=mask_inv_lsc)
    return results


def generateLSC_onbatch(srcDir: str,
                        distDir: str,
                        color: int = 1,
                        resize_shape=None,
                        iterate: int = 10,
                        mask: bool = False,
                        on_img: bool = True,
                        number: bool = False,
                        ):
    if mask:
        create_directory(os.path.join(distDir, "mask"))
    if on_img:
        create_directory(os.path.join(distDir, "superpixel_img"))
    if number:
        create_directory(os.path.join(distDir, "meta"))
    numberPath = os.path.join(distDir, "meta", "superpixel_count.json")
    numberDict = dict()
    img_files = os.listdir(srcDir)
    img_paths = [os.path.join(srcDir, f) for f in img_files]
    for i, img in enumerate(img_paths):
        try:
            maskPath = os.path.join(distDir, "mask", img_files[i])
            on_imgPath = os.path.join(distDir, "superpixel_img", img_files[i])
            img = cv2.imread(img_paths[i], flags=color)
            if resize_shape is not None:
                img = cv2.resize(img, resize_shape)
            lsh = LSC(img, iterate=iterate, mask=mask, on_img=on_img, number=number)
            if mask:
                cv2.imwrite(maskPath, lsh['mask'])
            if on_img:
                cv2.imwrite(on_imgPath, lsh['on_img'])
            if number:
                numberDict[img_paths[i]] = lsh['number']
        except Exception:
            print("pass {}".format(img_paths[i]))
            continue
    write_json(numberPath, numberDict)


def splitSuperpixel(dirPath: str,
                    color: int = 1,
                    resize_shape=None,
                    iterate: int = 10,
                    mask: bool = False,
                    on_img: bool = True,
                    number: bool = False):
    files = os.listdir(dirPath)
    img_path = os.path.join(dirPath, 'img')
    if not os.path.exists(img_path):
        os.mkdir(img_path)
        for file in files:
            if os.path.isfile(os.path.join(dirPath, file)):
                shutil.move(os.path.join(dirPath, file), os.path.join(img_path, file))
    if mask:
        mask_path = os.path.join(dirPath, 'mask')
        create_directory(mask_path)
        clear_directory(mask_path)

    if on_img:
        on_img_path = os.path.join(dirPath, 'superpixel_img')
        create_directory(on_img_path)
        clear_directory(on_img_path)

    if number:
        number_path = os.path.join(dirPath, 'meta')
        create_directory(on_img_path)
        clear_directory(on_img_path)
    generateLSC_onbatch(img_path, dirPath, color=color, resize_shape=resize_shape, iterate=iterate, mask=mask,
                        on_img=on_img)
