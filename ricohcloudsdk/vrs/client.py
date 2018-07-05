# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

"""
RICOH Cloud API Visual Recognition
"""
import os
import json
from ricohcloudsdk.auth.client import AuthClient
from .util import request, get_type, raise_combination_error, SUPPORTED_IMAGE_TYPE


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

    def __send_request(self, http_method, api_path, request_type=None, resource=None):
        uri = VisualRecognition.__ENDPOINT + api_path
        headers = self.__get_common_headers()
        if not request_type and not resource:
            headers['Content-Type'] = VisualRecognition.__CTYPE_JSON
            return request(http_method, uri, headers=headers)
        resource_type = get_type(resource)
        if request_type == 'multipart':
            if resource_type == 'uri':
                headers['Content-Type'] = VisualRecognition.__CTYPE_JSON
                payload = json.dumps({
                    'image': resource
                })
                ret = request(http_method, uri, headers=headers, data=payload)
            else:
                with open(resource, 'rb') as src_img:
                    file_payload = {
                        'image': src_img,
                    }
                    ret = request(http_method, uri, headers=headers,
                                  files=file_payload)
        elif request_type == 'image':
            if resource_type == 'uri':
                headers['Content-Type'] = VisualRecognition.__CTYPE_JSON
                payload = json.dumps({
                    'image': resource
                })
                ret = request(http_method, uri, headers=headers, data=payload)
            else:
                headers['Content-Type'] = 'image/' + resource_type
                with open(resource, 'rb') as payload:
                    ret = request(http_method, uri,
                                  headers=headers, data=payload)
        return ret

    def __send_compare_request(self, http_method, source, target, max_results):
        uri = VisualRecognition.__ENDPOINT + '/compare_faces'
        headers = self.__get_common_headers()
        src_type = get_type(source)
        tar_type = get_type(target)
        if src_type == 'uri' and tar_type == 'uri':
            headers['Content-Type'] = VisualRecognition.__CTYPE_JSON
            payload = json.dumps({
                'source': source,
                'target': target
            })
            ret = request(http_method, uri, headers=headers, data=payload)
        elif src_type in SUPPORTED_IMAGE_TYPE and tar_type in SUPPORTED_IMAGE_TYPE:
            with open(source, 'rb') as src_img, open(target, 'rb') as tar_img:
                file_payload = {
                    'source': src_img,
                    'target': tar_img
                }
                ret = request(http_method, uri, headers=headers,
                              files=file_payload)
        elif src_type == 'uri' and tar_type == 'uuid':
            payload = {'image': source}
            if max_results:
                payload['max_results'] = max_results
            uri = uri + '/' + target
            headers['Content-Type'] = VisualRecognition.__CTYPE_JSON
            ret = request(http_method, uri, headers=headers,
                          data=json.dumps(payload))
        elif src_type in SUPPORTED_IMAGE_TYPE and tar_type == 'uuid':
            uri = uri + '/' + target
            with open(source, 'rb') as src_img:
                file_payload = {
                    'image': src_img,
                }
                if max_results:
                    data_payload = {
                        'max_results': max_results
                    }
                    ret = request(http_method, uri, headers=headers,
                                  data=data_payload, files=file_payload)
                else:
                    ret = request(http_method, uri, headers=headers,
                                  files=file_payload)
        else:
            raise_combination_error()

        return ret

    def detect_faces(self, resource):
        """Detect face."""
        api_path = '/detect_faces'
        res = self.__send_request('POST', api_path, 'image', resource)
        return res

    def detect_humans(self, resource):
        """Detect humas."""
        api_path = '/detect_humans'
        res = self.__send_request('POST', api_path, 'image', resource)
        return res

    def compare_faces(self, source, target, max_results=None):
        """Compare faces."""
        res = self.__send_compare_request('POST', source, target, max_results)
        return res

    def add_face(self, resource, collection_id):
        """Add face to collecton."""
        api_path = '/face_collections/{}/faces'.format(collection_id)
        res = self.__send_request('POST', api_path, 'multipart', resource)
        return res

    def create_collection(self):
        """Create face collection."""
        api_path = '/face_collections'
        res = self.__send_request('POST', api_path)
        return res

    def list_collections(self):
        """List stored face collection."""
        api_path = '/face_collections'
        res = self.__send_request('GET', api_path)
        return res

    def list_faces(self, collection_id):
        """List stored faces on the face collection."""
        api_path = '/face_collections/{}/faces'.format(collection_id)
        res = self.__send_request('GET', api_path)
        return res

    def delete_collection(self, collection_id):
        """Delete face collection."""
        api_path = '/face_collections/{}'.format(collection_id)
        res = self.__send_request('DELETE', api_path)
        return res

    def remove_face(self, collection_id, face_id):
        """Remove face from the face collection."""
        api_path = '/face_collections/{}/faces/{}'.format(
            collection_id, face_id)
        res = self.__send_request('DELETE', api_path)
        return res
