# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

"""Add face to face collection sample."""
from __future__ import print_function

import os
import json
import argparse
from PIL import Image, ImageDraw
from vr_utils import create_vrs_client, draw_rectangle


def get_collection_id(vrs_client):
    """Get ID of the stored face collection or creates a face collection if it doesn't exists.

    :param vrs_client: instance of the VisualRecognition class
    """
    res = vrs_client.list_collections()
    if res['face_collections']:
        face_collection = res['face_collections'][0]
    else:
        res = vrs_client.create_collection()
        face_collection = res
    return face_collection['collection_id']


def add_face(pil_img, file_path):
    """Add face to face collection.

    :param pil_img: image object from PIL.Image
    :param file_path: image file path
    """
    vrs_client = create_vrs_client()

    draw = ImageDraw.Draw(pil_img)
    collection_id = get_collection_id(vrs_client)
    response = vrs_client.add_face(file_path, collection_id)
    draw_rectangle(response['location'], draw)
    save_dir = './results/{0}'.format(collection_id)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    pil_img.save('{0}/{1}.jpg'.format(save_dir,
                                      response['face_id']), quality=90)
    print(json.dumps(response, indent=4, separators=(',', ': ')))


def main():
    parser = argparse.ArgumentParser(
        description='create face collection and add face sample')
    parser.add_argument('-f', '--file', type=str, dest='file_path',
                        help='specify image resource (JPEG or PNG) to process')
    args = parser.parse_args()

    if args.file_path is None:
        parser.print_help()
        return
    try:
        pil_img = Image.open(args.file_path)
    except IOError:
        raise

    add_face(pil_img, args.file_path)


if __name__ == '__main__':
    main()
