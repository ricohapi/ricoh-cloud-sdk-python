# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

"""
Utility for the Visual Recognition
"""
import os
import json
import re
import requests
from urllib3.util.retry import Retry
from PIL import Image
from requests.adapters import HTTPAdapter
from ricohcloudsdk.exceptions import ClientError, ServerError

SUPPORTED_IMAGE_TYPE = {'jpeg', 'png'}
UNSUPPORTED_ERROR = 'One of the resource was unsupported format.'
RESOURCE_ERROR = 'An invalid value was specified for one of the resource parameters.'
COMBINATION_ERROR = 'Different combinations for resource format are not allowed.'

RETRY_TOTAL = 3
BACKOFF_FACTOR = 1
METHOD_WHITELIST = ['GET', 'POST', 'DELETE']
STATUS_FORCELIST = [408, 500, 502, 503, 504]
RETRIES = Retry(
    total=RETRY_TOTAL,
    backoff_factor=BACKOFF_FACTOR,
    method_whitelist=METHOD_WHITELIST,
    status_forcelist=STATUS_FORCELIST
)
SESSION = requests.Session()
SESSION.mount('http://', HTTPAdapter(max_retries=RETRIES))

UUID = '\A[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\Z'


def raise_unsupported_error():
    raise ValueError(UNSUPPORTED_ERROR)


def raise_resource_error():
    raise ValueError(RESOURCE_ERROR)


def raise_combination_error():
    raise ValueError(COMBINATION_ERROR)


def get_type(resource):
    """Check the resource type."""
    if os.path.isfile(resource):
        img = Image.open(resource)
        img_type = img.format.lower()
        if img_type not in SUPPORTED_IMAGE_TYPE:
            raise_unsupported_error()
        r_type = img_type
    elif re.match(r'^https?:\/\/', resource):
        r_type = 'uri'
    elif re.match(UUID, resource):
        r_type = 'uuid'
    else:
        raise_resource_error()
    return r_type


def request(http_method, uri, **kwargs):
    """Send data to the API endpoint and receive the result."""
    req = SESSION.request(http_method, uri, **kwargs)
    try:
        ret = json.loads(req.text)
    except ValueError:
        ret = req.text
    if 400 <= req.status_code < 500:
        raise ClientError(req.status_code, ret)
    elif req.status_code >= 500:
        raise ServerError(req.status_code, ret)
    return ret
