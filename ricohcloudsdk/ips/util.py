# -*- coding: utf-8 -*-
# Copyright (c) 2018 Ricoh Co., Ltd. All Rights Reserved.

"""
Utility for the Image Processing
"""
import os
import imghdr
import json
import re
import requests
from ricohcloudsdk.exceptions import ClientError, ServerError

SUPPORTED_IMAGE_TYPE = {'jpeg', 'png'}
UNSUPPORTED_ERROR = 'One of the image resource was unsupported format.'
RESOURCE_ERROR = 'An invalid value was specified for one of the image resource parameters.'


def raise_unsupported_error():
    raise ValueError(UNSUPPORTED_ERROR)


def raise_resource_error():
    raise ValueError(RESOURCE_ERROR)


def get_type(resource):
    """Check the resource type."""
    if os.path.isfile(resource):
        image_type = imghdr.what(resource)
        if image_type not in SUPPORTED_IMAGE_TYPE:
            raise_unsupported_error()
        r_type = image_type
    elif re.match(r'^https?:\/\/', resource):
        r_type = 'uri'
    else:
        raise_resource_error()
    return r_type


def post(api_path, **kwargs):
    """Send data to the API endpoint and receive the result."""
    r = requests.post(api_path, **kwargs)
    if r.status_code < 400:
        return r
    try:
        ret = json.loads(r.text)
    except ValueError:
        ret = r.text
    if 400 <= r.status_code < 500:
        raise ClientError(r.status_code, ret)
    else:
        raise ServerError(r.status_code, ret)
