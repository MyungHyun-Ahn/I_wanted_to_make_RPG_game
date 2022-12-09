"""
스프라이트 시트 자르기 툴 pillow 라이브러리 활용
"""

from PIL import Image
import math
import os

def vertical_slice(image_path, outdir, slice_size):
    img = Image.open(image_path)
    width, height = img.size
    print(width, height)
    upper = 0
    left = 0
    slices = int(math.ceil(height/slice_size))
    count = 1
    for slice in range(slices):
        if count == slices:
            lower = height
        else:
            lower = int(count * slice_size)

        bbox = (left, upper, width, lower)
        working_slice = img.crop(bbox)
        upper += slice_size
        output = "{}/{}.png".format(outdir, count - 1)
        working_slice.save(output)
        count += 1


def horizontal_slice(image_path, outdir, slice_size, num):
    img = Image.open(image_path)
    width, height = img.size
    upper = 0
    left = 0
    slices = int(math.ceil(width/slice_size))
    count = 1
    for slice in range(slices):
        if count == slices:
            right = width
        else:
            right = int(count * slice_size)  
        bbox = (left, upper, right, height)
        working_slice = img.crop(bbox)
        size = working_slice.size
        working_slice = working_slice.resize((size[0] * 4, size[1] * 4))
        print((size[0] * 4, size[1] * 4))
        left += slice_size
        if count == 1:
            output = "{}/down/{}.png".format(outdir, num)
        elif count == 2:
            output = "{}/up/{}.png".format(outdir, num)
        elif count == 3:
            output = "{}/right/{}.png".format(outdir, num)
        else:
            output = "{}/left/{}.png".format(outdir, num)
        working_slice.save(output)
        count += 1


def png_size_converter(image_path, outdir, out_name, px, py):
    img = Image.open(image_path)
    img = img.resize((px, py))
    output = "{}/{}.png".format(outdir, out_name)
    img.save(output)



def image_slicer(file_path):
    vertical_slice(file_path, 'tools/output/intermediate', 16) # 중간파일 세로로 자르기
    for i in range(4):
        horizontal_slice('tools/output/intermediate/{}.png'.format(i), 'tools/output/final', 16, i) # 최종파일 가로로 자르기


def weapon_img_converter(image_path, outdir):
    img = Image.open(image_path)
    for i in range(4):
        if i != 0:
            img = img.transpose(Image.ROTATE_90)
        output = "{}/{}.png".format(outdir, i)
        img.save(output)


# image_slicer('tools/SpriteSheet.png')

png_size_converter("tools/Club/0.png", 'tools/Club', 'c0', 32, 14 * 4)
png_size_converter("tools/Club/1.png", 'tools/Club', 'c1', 32, 14 * 4)

weapon_img_converter("tools/Club/c1.png", 'tools/Club/final')



