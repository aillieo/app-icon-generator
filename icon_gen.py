#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
icon_gen (https://github.com/aillieo/app-icon-generator)
Fast and easy way to generate icons for iOS and Android apps
Created by Aillieo on 2017-08-10
With Python 3.5
"""

from PIL import Image
import os

path_iOS = ['Icon-57', 'Icon-114']
size_iOS = [57, 114]
dict_iOS = zip(path_iOS, size_iOS)
path_Android = ['drawable-hdpi/icon', 'drawable-mdpi/icon']
size_Android = [72, 48]
dict_Android = zip(path_Android, size_Android)
path_custom = ['my_icon', 'your_icon']
size_custom = [60, 90]
dict_custom = zip(path_custom, size_custom)

gen_for_iOS = False
gen_for_Android = False
param_rounded = 0.0
param_outline = 0.0
need_rounded = False
need_outline = False


def get_gen_options():
    """collect gen options including icons for iOS or Android, whether rounded icon or outlined icon"""
    pass


def get_ref_file():
    """get reference image by finding one image file in current directory or manually input"""
    files = os.listdir()
    ref_file = ''
    for filename in files:
        if filename.split('.')[-1] == 'png':
            ref_file = filename
            break
    if ref_file:
        print('will use %s as reference image' % ref_file)
    else:
        print('can not find property file, now please specific one')
        ref_file = input('input file name:')
    if not os.path.exists(ref_file):
        raise IOError('file not found: ' + ref_file)
    return ref_file


def gen_template_img(ref_file):
    """get template image for later resizing"""
    ref_img = Image.open(ref_file)
    template_img = ref_img
    if need_rounded:
        template_img = add_rounded(template_img)
    if need_outline:
        template_img = add_outline(template_img)
    return template_img


def gen_icons(template_img):
    """generate icons by resizing template image according to sizes defined in size list"""
    for name, size in dict_iOS:
        name += '.png'
        out_img = template_img.resize((size, size), Image.BILINEAR)
        try:
            out_img.save(name, 'PNG')
        except IOError:
            print("IOError: save file failed" + name)


def add_rounded(img_in):
    """rounding corner for template"""
    img_out = img_in
    return img_out


def add_outline(img_in):
    """add outline for template"""
    img_out = img_in
    return img_out


if __name__ == '__main__':
    file = get_ref_file()
    get_gen_options()
    img = gen_template_img(file)
    gen_icons(img)
