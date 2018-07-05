# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

"""Compare face to collection sample."""
from __future__ import print_function

import argparse
import json
from PIL import Image, ImageDraw
from vr_utils import create_vrs_client, draw_rectangle, get_collection_id, ClientError


def compare_faces(pil_img, file_path, max_results=None):
    """Compare face to collection.

    :param pil_img: image object from PIL.Image
    :param file_path: image file path
    :param max_results:　a value to limit the result to be displayed
    """
    vrs_client = create_vrs_client()
    collection_id = get_collection_id(vrs_client)
    response = vrs_client.compare_faces(
        file_path, collection_id, max_results)
    source_draw = ImageDraw.Draw(pil_img)
    draw_rectangle(response['source']['location'], source_draw)
    pil_img.save(
        './results/compare_face_to_{0}.jpg'.format(collection_id), quality=90)
    print(json.dumps(response, indent=4, separators=(',', ': ')))


def main():
    parser = argparse.ArgumentParser(
        description='compare face to collection sample')
    parser.add_argument('-f', '--file', type=str, dest='file_path',
                        help='specify image file (JPEG or PNG) to process')
    parser.add_argument('--max_results', type=str, dest='max_results',
                        help='The valid range is 1 ~ 1000. The default is 10.')
    args = parser.parse_args()
    if args.file_path is None:
        parser.print_help()
        return

    try:
        pil_img = Image.open(args.file_path)
        compare_faces(pil_img, args.file_path)
    except ClientError as error:
        print(error.message)
    except IOError:
        raise


if __name__ == '__main__':
    main()
