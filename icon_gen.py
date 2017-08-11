# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
icon_gen (https://github.com/aillieo/app-icon-generator)
Fast and easy way to generate icons for iOS and Android apps
Created by Aillieo on 2017-08-10
With Python 3.5
"""

from PIL import Image
import os

# output path and size config:
path_iOS = ['Icon-57', 'Icon-114']
size_iOS = [57, 114]
path_Android = ['drawable-hdpi/icon', 'drawable-mdpi/icon']
size_Android = [72, 48]
path_custom = ['my_icon', 'your_icon']
size_custom = [60, 90]
dict_iOS = zip(path_iOS, size_iOS)
dict_Android = zip(path_Android, size_Android)
dict_custom = zip(path_custom, size_custom)

# generate options:
gen_for_iOS = True
gen_for_Android = True
param_rounded = float(90) / 512
param_outline = (float(30) / 512, 255, 255, 255)
need_rounded = True
need_outline = False


def get_gen_options():
    """collect gen options including icons for iOS or Android, whether rounded icon or outlined icon"""
    pass


def get_ref_file():
    """get reference image by finding one image file in current directory or manually input"""
    file_ext = ['png', 'jpg', 'jpeg']
    files = os.listdir()
    ref_file = ''
    for filename in files:
        if filename.split('.')[-1].lower() in file_ext:
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
    size = min(ref_img.width, ref_img.height)
    template_img = ref_img.resize((size, size), Image.BILINEAR)
    if need_rounded:
        template_img = add_rounded(template_img)
    if need_outline:
        template_img = add_outline(template_img)
    return template_img


def gen_icons(template_img, dict_path_size):
    """generate icons by resizing template image according to sizes defined in size list"""
    for name, size in dict_path_size:
        name = 'out/' + name + '.png'
        name = os.path.normpath(name)
        path, base = os.path.split(name)
        if path and not os.path.exists(path):
            os.makedirs(path)
        out_img = template_img.resize((size, size), Image.BILINEAR)
        try:
            out_img.save(name, 'PNG')
        except IOError:
            print("IOError: save file failed" + name)


def add_rounded(img_in):
    """rounding corner for template"""
    if img_in.mode != 'RGBA':
        img_in = img_in.convert('RGBA')
    size = img_in.size[0]
    radius = size * param_rounded
    if radius > 0:
        img_in.load()
        for i in range(size):
            for j in range(size):
                if will_cut_off(size, radius, i, j):
                    img_in.putpixel((i, j), (0, 0, 0, 0))
    img_out = img_in
    return img_out


def add_outline(img_in):
    """add outline for template"""
    img_out = img_in
    return img_out


def will_cut_off(size, radius, x, y):
    """judge whether a point should be transparent"""
    center = (0, 0)
    if x < radius and y < radius:
        center = (radius, radius)
    elif x < radius and y > size - radius:
        center = (radius, size - radius)
    elif x > size - radius and y < radius:
        center = (size - radius, radius)
    elif x > size - radius and y > size - radius:
        center = (size - radius, size - radius)

    if center != (0, 0):
        if (x - center[0]) ** 2 + (y - center[1]) ** 2 > radius ** 2:
            return True
    return False


if __name__ == '__main__':
    file = get_ref_file()
    get_gen_options()
    img = gen_template_img(file)
    if gen_for_iOS:
        print('geneRating for iOS ...')
        gen_icons(img, dict_iOS)
    if gen_for_Android:
        print('geneRating for Android ...')
        gen_icons(img, dict_Android)
    if not gen_for_iOS and not gen_for_Android:
        print('geneRating custom icons ...')
        gen_icons(img, dict_custom)
    print('finished icon generation!')
