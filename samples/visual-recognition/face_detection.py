# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

"""Face detection sample."""
import os
import argparse
from PIL import Image, ImageDraw
from vr_utils import create_vrs_client, draw_rectangle


def face_detection(pil_img, file_path):
    """Call face detection API and show the processed image.

    :param pil_img: image object from PIL.Image
    :param file_path: image file path
    """
    vrs_client = create_vrs_client()
    draw = ImageDraw.Draw(pil_img)
    response = vrs_client.detect_faces(file_path)
    faces_list = response["faces"]
    for face in faces_list:
        draw_rectangle(face['location'], draw)
    if not os.path.exists('./results'):
        os.mkdir('./results')
    pil_img.save('./results/face_detection.jpg', quality=90)


def main():
    parser = argparse.ArgumentParser(description='Face detection sample')
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

    face_detection(pil_img, args.file_path)


if __name__ == '__main__':
    main()
