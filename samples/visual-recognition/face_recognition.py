# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

"""Face recognition sample."""
from __future__ import print_function

import os
import argparse
from PIL import Image, ImageDraw
from vr_utils import create_vrs_client, draw_rectangle


def compare_faces(source_pil_img, target_pil_img, source_path, target_path):
    """Call face recognition API and show the processed image.

    :param source_pil_img: source image object from PIL.Image
    :param target_pil_img: target image object from PIL.Image
    :param source_path: source image file path
    :param target_path: target image file path
    """
    vrs_client = create_vrs_client()
    resp = vrs_client.compare_faces(source_path, target_path)
    source_draw = ImageDraw.Draw(source_pil_img)
    target_draw = ImageDraw.Draw(target_pil_img)
    draw_rectangle(resp['source']['location'], source_draw)
    draw_rectangle(resp['target']['location'], target_draw)
    if not os.path.exists('./results'):
        os.mkdir('./results')
    source_pil_img.save('./results/face_recognition_source.jpg', quality=90)
    target_pil_img.save('./results/face_recognition_target.jpg', quality=90)
    print('score: {0}'.format(resp['score']))


def main():
    parser = argparse.ArgumentParser(description='face recognition sample')
    parser.add_argument('-s', '--source', type=str, dest='source_path',
                        help='specify image file (JPEG or PNG) to process')
    parser.add_argument('-t', '--target', type=str, dest='target_path',
                        help='specify image file (JPEG or PNG) to process')
    args = parser.parse_args()
    if args.source_path is None or args.target_path is None:
        parser.print_help()
        return

    try:
        source_pil_img = Image.open(args.source_path)
        target_pil_img = Image.open(args.target_path)
    except IOError:
        raise

    compare_faces(source_pil_img, target_pil_img,
                  args.source_path, args.target_path)


if __name__ == '__main__':
    main()
