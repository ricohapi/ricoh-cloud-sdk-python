# -*- coding: utf-8 -*-
# Copyright (c) 2018 Ricoh Co., Ltd. All Rights Reserved.

"""
RICOH Cloud API Image Processing
"""
import os
import json
from ricohcloudsdk.auth.client import AuthClient
from . import util


class ImageProcessing(object):
    """image processing client"""
    __ENDPOINT = 'https://vps.api.ricoh/v1'
    __SCOPE = AuthClient.SCOPES['ips']
    __CTYPE_JSON = 'application/json'

    def __init__(self, aclient):
        self.__aclient = aclient
        self.__aclient.session(ImageProcessing.__SCOPE)

    def __get_common_headers(self):
        return {
            'Authorization': 'Bearer ' + self.__aclient.get_access_token(),
            'x-api-key': self.__aclient.get_api_key()
        }

    def filter(self, resource, parameters):
        api_path = ImageProcessing.__ENDPOINT + '/filter'
        headers = self.__get_common_headers()
        headers['Accept'] = 'image/jpeg'
        r_type = util.get_type(resource)
        if r_type == 'uri':
            headers['Content-Type'] = ImageProcessing.__CTYPE_JSON
            payload = json.dumps({
                'image': resource,
                'parameters': parameters
            })
            ret = util.post(api_path, headers=headers, data=payload)
        else:
            data = {'parameters': json.dumps(parameters)}
            with open(resource, 'rb') as image:
                ctype = 'image/' + r_type
                filename = os.path.basename(resource)
                files = {'image': (filename, image, ctype)}
                ret = util.post(api_path, headers=headers,
                                files=files, data=data)
        return ret.content
