# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

"""
Utility for the Visual Recognition
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
COMBINATION_ERROR = 'Different combinations for image resource format are not allowed.'


def raise_unsupported_error():
    raise ValueError(UNSUPPORTED_ERROR)


def raise_resource_error():
    raise ValueError(RESOURCE_ERROR)


def raise_combination_error():
    raise ValueError(COMBINATION_ERROR)


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
    req = requests.post(api_path, **kwargs)
    try:
        ret = json.loads(req.text)
    except ValueError:
        ret = req.text
    if 400 <= req.status_code < 500:
        raise ClientError(req.status_code, ret)
    elif req.status_code >= 500:
        raise ServerError(req.status_code, ret)
    return ret
