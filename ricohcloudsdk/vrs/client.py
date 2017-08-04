# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

"""
RICOH Cloud API Visual Recognition
"""
import json
from ricohcloudsdk.auth.client import AuthClient
from . import util


class VisualRecognition(object):
    """visual recognition client"""
    __ENDPOINT = 'https://ips.api.ricoh/v1'
    __SCOPE = AuthClient.SCOPES['vrs']
    __CTYPE_JSON = 'application/json'

    def __init__(self, aclient):
        self.__aclient = aclient
        self.__aclient.session(VisualRecognition.__SCOPE)

    def __get_common_headers(self):
        return {
            'Authorization': 'Bearer ' + self.__aclient.get_access_token(),
            'x-api-key': self.__aclient.get_api_key()
        }

    def __send_detect(self, api_path, resource):
        api_path = VisualRecognition.__ENDPOINT + api_path
        headers = self.__get_common_headers()
        r_type = util.get_type(resource)

        if r_type == 'uri':
            headers['Content-Type'] = VisualRecognition.__CTYPE_JSON
            payload = json.dumps({
                'image': resource
            })
            ret = util.post(api_path, headers=headers, data=payload)
        else:
            headers['Content-Type'] = 'image/' + r_type
            with open(resource, 'rb') as payload:
                ret = util.post(api_path, headers=headers, data=payload)
        return ret

    def __send_compare(self, source, target):
        api_path = VisualRecognition.__ENDPOINT + '/compare_faces'
        headers = self.__get_common_headers()
        src_type = util.get_type(source)
        tar_type = util.get_type(target)

        if src_type == 'uri' and tar_type == 'uri':
            headers['Content-Type'] = VisualRecognition.__CTYPE_JSON
            payload = json.dumps({
                'source': source,
                'target': target
            })
            ret = util.post(api_path, headers=headers, data=payload)
        elif src_type in util.SUPPORTED_IMAGE_TYPE and tar_type in util.SUPPORTED_IMAGE_TYPE:
            with open(source, 'rb') as src_img, open(target, 'rb') as tar_img:
                file_payload = {
                    'source': src_img,
                    'target': tar_img
                }
                ret = util.post(api_path, headers=headers, files=file_payload)
        else:
            util.raise_combination_error()

        return ret

    def detect_faces(self, resource):
        """Face detection method."""
        res = self.__send_detect('/detect_faces', resource)
        return res

    def detect_humans(self, resource):
        """Human detection method."""
        res = self.__send_detect('/detect_humans', resource)
        return res

    def compare_faces(self, source, target):
        """Face recognition method."""
        res = self.__send_compare(source, target)
        return res
