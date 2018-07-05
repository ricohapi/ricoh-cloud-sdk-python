# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

"""Utility for visual recognition samples."""
from __future__ import print_function

import json
from ricohcloudsdk.auth.client import AuthClient
from ricohcloudsdk.vrs.client import VisualRecognition


MESSAGE_NOT_CREATED_COLLECTION = (
    'Not created face collection yet.'
    'Please add face to collection using add_face_to_collection.py in advance.')


class ClientError(Exception):

    def __init__(self, message):
        self.message = message


def create_vrs_client():
    """Read config file and creates client for visual recognition SDK."""
    with open('./config.json', 'r') as settings:
        config = json.load(settings)
        client_id = config['CLIENT_ID']
        client_secret = config['CLIENT_SECRET']

    auth_client = AuthClient(client_id, client_secret)
    vrs_client = VisualRecognition(auth_client)
    return vrs_client


def draw_rectangle(rectangle, draw):
    """Draw rectangle.

    :param rectangle: dictionary of the rectangle {left, top, bottom, right}
    :param draw: instance of the PIL.ImageDraw class
    """
    left = rectangle['left']
    top = rectangle['top']
    right = rectangle['right']
    bottom = rectangle['bottom']
    draw.rectangle(((left, top), (right, bottom)),
                   outline=(255, 0, 0), fill=None)


def get_collection_id(vrs_client):
    """Get ID of the stored face collection.

    :param vrs_client: instance of the VisualRecognition class
    """
    response = vrs_client.list_collections()
    if response['face_collections']:
        face_collection = response['face_collections'][0]
    else:
        raise ClientError(MESSAGE_NOT_CREATED_COLLECTION)
    return face_collection['collection_id']
