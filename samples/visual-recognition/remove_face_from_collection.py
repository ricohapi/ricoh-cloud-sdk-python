# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

"""Remove face from face collection sample."""
from __future__ import print_function

import argparse
import os
from vr_utils import create_vrs_client, get_collection_id, ClientError


def remove_face(face_id):
    """Remove face from face collection and delete local image.

    :param face_id: id of the face
    """
    vrs_client = create_vrs_client()
    collection_id = get_collection_id(vrs_client)
    vrs_client.remove_face(collection_id, face_id)
    save_dir = './results/{0}/{1}.jpg'.format(collection_id, face_id)
    if os.path.exists(save_dir):
        os.remove(save_dir)


def main():
    parser = argparse.ArgumentParser(
        description='remove face from face collection sample')
    parser.add_argument('--face_id', type=str, dest='face_id',
                        help='ID of the face')
    args = parser.parse_args()
    if args.face_id is None:
        parser.print_help()
        return

    try:
        remove_face(args.face_id)
    except ClientError as error:
        print(error.message)


if __name__ == '__main__':
    main()
