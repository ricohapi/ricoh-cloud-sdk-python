# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

"""Human detection sample."""
import os
import argparse
from PIL import Image, ImageDraw
from vr_utils import create_vrs_client, draw_rectangle


def human_detection(pil_img, file_path):
    """Call human detection API and show the processed image.

    :param pil_img: image object from PIL.image
    :param file_path: image file path
    """
    vrs_client = create_vrs_client()
    draw = ImageDraw.Draw(pil_img)
    res = vrs_client.detect_humans(file_path)
    humans_list = res["humans"]
    for human in humans_list:
        draw_rectangle(human['location'], draw)
    if not os.path.exists('./results'):
        os.mkdir('./results')
    pil_img.save('./results/human_detection.jpg', quality=90)


def main():
    parser = argparse.ArgumentParser(description='Human detection sample')
    parser.add_argument('-f', '--file', type=str, dest='file_path',
                        help='specify image file (JPEG or PNG) to process')
    args = parser.parse_args()
    if args.file_path is None:
        parser.print_help()
        return
    try:
        pil_img = Image.open(args.file_path)
    except IOError:
        raise
    human_detection(pil_img, args.file_path)


if __name__ == '__main__':
    main()
