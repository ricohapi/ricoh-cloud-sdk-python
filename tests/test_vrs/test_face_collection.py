# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

import os
from unittest import TestCase
import json
import pytest
import mock
from mock import Mock, MagicMock
from requests.exceptions import RequestException
from ricohcloudsdk.vrs import util
from ricohcloudsdk.vrs.client import VisualRecognition
from ricohcloudsdk.exceptions import ClientError

ENDPOINT = 'https://ips.api.ricoh/v1'


def make_headers(c_type):
    headers = {
        'Authorization': 'Bearer atoken',
        'x-api-key': 'apikey',
        'Content-Type': c_type
    }
    return headers


class TestInit(TestCase):

    def setUp(self):
        self.aclient = Mock()
        self.aclient.session = Mock(return_value={'access_token': 'atoken'})

    def test_ok(self):
        VisualRecognition(self.aclient)

    def test_param_err(self):
        with pytest.raises(TypeError):
            VisualRecognition()


class TestMethodOK(TestCase):

    def setUp(self):
        self.aclient = Mock()
        self.aclient.get_access_token = Mock(return_value='atoken')
        self.aclient.get_api_key = Mock(return_value='apikey')
        self.aclient.session = Mock(return_value={'access_token': 'atoken'})
        self.vrs = VisualRecognition(self.aclient)
        self.__create_face_collection_expected = {
            'collection_id': '728bee35-fa67-473b-91bf-79f088f46179'
        }
        self.__list_face_collections_expected = {
            'face_collections': [
                {
                    'collection_id': '728bee35-fa67-473b-91bf-79f088f46179'
                }
            ]
        }
        self.__list_faces_expected = {
            'faces': [
                {
                    'face_id': '728bee35-fa67-473b-91bf-79f088f46179'
                }
            ]
        }
        self.__add_face_expected = {
            'face_id': '728bee35-fa67-473b-91bf-79f088f46179',
            'location': {
                'left': 1085,
                'top': 244,
                'right': 1307,
                'bottom': 466
            }
        }
        self.__compare_face_to_collection_expected = {
            'source': {
                'location': {
                    'left': 1085,
                    'top': 244,
                    'right': 1307,
                    'bottom': 466
                }
            },
            'target': {
                'collection_id': '80bf2bdc-d3de-491e-9106-0635df0a0a18',
                'faces': [
                    {
                        'face_id': '80bf2bdc-d3de-491e-9106-0635df0a0a18',
                        'score': 0.787753701210022,
                    }
                ]
            }
        }

    def test_param_err(self):
        with pytest.raises(TypeError):
            self.vrs.detect_faces()

    @mock.patch('ricohcloudsdk.vrs.util.SESSION.request')
    def test_list_collection(self, req):
        req.return_value.text = json.dumps(
            self.__list_face_collections_expected)
        req.return_value.status_code = 200
        assert self.__list_face_collections_expected == self.vrs.list_collections()
        headers = make_headers('application/json')
        req.assert_called_once_with(
            'GET', ENDPOINT + '/face_collections', headers=headers)

    @mock.patch('ricohcloudsdk.vrs.util.SESSION.request')
    def test_create_collection(self, req):
        req.return_value.text = json.dumps(
            self.__create_face_collection_expected)
        req.return_value.status_code = 201
        assert self.__create_face_collection_expected == self.vrs.create_collection()
        headers = make_headers('application/json')
        req.assert_called_once_with(
            'POST', ENDPOINT + '/face_collections', headers=headers)

    @mock.patch('ricohcloudsdk.vrs.util.SESSION.request')
    def test_delete_collection(self, req):
        req.return_value.text = ''
        req.return_value.status_code = 204
        assert '' == self.vrs.delete_collection(
            '728bee35-fa67-473b-91bf-79f088f46179')
        headers = make_headers('application/json')
        uri = '/face_collections/728bee35-fa67-473b-91bf-79f088f46179'
        req.assert_called_once_with(
            'DELETE', ENDPOINT + uri, headers=headers)

    @mock.patch('ricohcloudsdk.vrs.util.SESSION.request')
    def test_list_faces(self, req):
        req.return_value.text = json.dumps(self.__list_faces_expected)
        req.return_value.status_code = 200
        assert self.__list_faces_expected == self.vrs.list_faces(
            '728bee35-fa67-473b-91bf-79f088f46179')
        headers = make_headers('application/json')
        uri = '/face_collections/728bee35-fa67-473b-91bf-79f088f46179/faces'
        req.assert_called_once_with(
            'GET', ENDPOINT + uri, headers=headers)

    @mock.patch('ricohcloudsdk.vrs.util.SESSION.request')
    def test_remove_face(self, req):
        req.return_value.text = ''
        req.return_value.status_code = 204
        assert '' == self.vrs.remove_face(
            '728bee35-fa67-473b-91bf-79f088f46179', '79a68ab3-8c42-4c79-bc09-3ac363cd9ab1')
        headers = make_headers('application/json')
        uri = '/face_collections/728bee35-fa67-473b-91bf-79f088f46179/faces/79a68ab3-8c42-4c79-bc09-3ac363cd9ab1'
        req.assert_called_once_with(
            'DELETE', ENDPOINT + uri, headers=headers)

    @mock.patch('ricohcloudsdk.vrs.util.Image.open')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    @mock.patch('ricohcloudsdk.vrs.util.SESSION.request')
    def test_add_face_jpeg(self, req, opn, isfile, pil_open):
        req.return_value.text = json.dumps(self.__add_face_expected)
        req.return_value.status_code = 201
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        img = MagicMock()
        img.format.lower.side_effect = ['jpeg']
        pil_open.return_value = img
        assert self.__add_face_expected == self.vrs.add_face(
            'test.jpg', '728bee35-fa67-473b-91bf-79f088f46179')
        headers = {
            'Authorization': 'Bearer atoken',
            'x-api-key': 'apikey'
        }
        uri = '/face_collections/728bee35-fa67-473b-91bf-79f088f46179/faces'
        payload = {
            'image': opn()
        }
        req.assert_called_once_with(
            'POST', ENDPOINT + uri, headers=headers, files=payload)

    @mock.patch('ricohcloudsdk.vrs.util.Image.open')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    @mock.patch('ricohcloudsdk.vrs.util.SESSION.request')
    def test_add_face_png(self, req, opn, isfile, pil_open):
        req.return_value.text = json.dumps(self.__add_face_expected)
        req.return_value.status_code = 201
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        img = MagicMock()
        img.format.lower.side_effect = ['png']
        pil_open.return_value = img
        assert self.__add_face_expected == self.vrs.add_face(
            'test.png', '728bee35-fa67-473b-91bf-79f088f46179')
        headers = {
            'Authorization': 'Bearer atoken',
            'x-api-key': 'apikey'
        }
        uri = '/face_collections/728bee35-fa67-473b-91bf-79f088f46179/faces'
        payload = {
            'image': opn()
        }
        req.assert_called_once_with(
            'POST', ENDPOINT + uri, headers=headers, files=payload)

    @mock.patch('ricohcloudsdk.vrs.util.SESSION.request')
    def test_add_face_uri(self, req):
        req.return_value.text = json.dumps(self.__add_face_expected)
        req.return_value.status_code = 200
        assert self.__add_face_expected == self.vrs.add_face(
            'http://test.com/test.jpg', '728bee35-fa67-473b-91bf-79f088f46179')
        headers = make_headers('application/json')
        payload = json.dumps({'image': 'http://test.com/test.jpg'})
        uri = '/face_collections/728bee35-fa67-473b-91bf-79f088f46179/faces'
        req.assert_called_once_with(
            'POST', ENDPOINT + uri, headers=headers, data=payload)

    @mock.patch('ricohcloudsdk.vrs.util.SESSION.request')
    def test_compare_faces_uri_to_collection(self, req):
        req.return_value.text = json.dumps(
            self.__compare_face_to_collection_expected)
        req.return_value.status_code = 200
        assert self.__compare_face_to_collection_expected == self.vrs.compare_faces(
            'http://test.com/test_1.jpg', '728bee35-fa67-473b-91bf-79f088f46179')
        headers = make_headers('application/json')
        payload = json.dumps(
            {
                'image': 'http://test.com/test_1.jpg'
            }
        )
        uri = '/compare_faces/728bee35-fa67-473b-91bf-79f088f46179'
        req.assert_called_once_with(
            'POST', ENDPOINT + uri, headers=headers, data=payload)

    @mock.patch('ricohcloudsdk.vrs.util.Image.open')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    @mock.patch('ricohcloudsdk.vrs.util.SESSION.request')
    def test_compare_faces_image_to_collection(self, req, opn, isfile, pil_open):
        req.return_value.text = json.dumps(
            self.__compare_face_to_collection_expected)
        req.return_value.status_code = 200
        isfile.side_effect = [True, False]
        img = MagicMock()
        img.format.lower.side_effect = ['jpeg']
        pil_open.return_value = img
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        assert self.__compare_face_to_collection_expected == self.vrs.compare_faces(
            'test_1.jpg', '728bee35-fa67-473b-91bf-79f088f46179')
        headers = {
            'Authorization': 'Bearer atoken',
            'x-api-key': 'apikey'
        }
        payload = {
            'image': opn()
        }
        uri = '/compare_faces/728bee35-fa67-473b-91bf-79f088f46179'
        req.assert_called_once_with(
            'POST', ENDPOINT + uri, headers=headers, files=payload)


class TestMethodError(TestCase):

    def setUp(self):
        self.aclient = Mock()
        self.aclient.get_access_token = Mock(return_value='atoken')
        self.aclient.get_api_key = Mock(return_value='apikey')
        self.aclient.session = Mock(return_value={'access_token': 'atoken'})
        self.vrs = VisualRecognition(self.aclient)

    def test_add_face_file_not_found(self):
        with pytest.raises(ValueError) as excinfo:
            self.vrs.add_face('collection_id', 'image.jpg')
        assert util.RESOURCE_ERROR == str(excinfo.value)

    def test_add_face_file_not_found(self):
        with pytest.raises(ValueError) as excinfo:
            self.vrs.add_face('collection_id', 'image.jpg')
        assert util.RESOURCE_ERROR == str(excinfo.value)

    @mock.patch('ricohcloudsdk.vrs.util.Image.open')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    def test_compare_faces_uuid_jpeg(self, opn, isfile, pil_open):
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.side_effect = [False, True]
        img = MagicMock()
        img.format.lower.return_value = 'jpeg'
        pil_open.return_value = img
        with pytest.raises(ValueError) as excinfo:
            self.vrs.compare_faces(
                'ef0dce93-c2ac-4da5-bb2c-82ca7c770ad8', 'test_1.jpeg'
            )
        assert util.COMBINATION_ERROR == str(excinfo.value)

    @mock.patch('ricohcloudsdk.vrs.util.Image.open')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    def test_compare_faces_uuid_uri(self, opn, isfile, pil_open):
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.side_effect = [False, False]
        with pytest.raises(ValueError) as excinfo:
            self.vrs.compare_faces(
                'ef0dce93-c2ac-4da5-bb2c-82ca7c770ad8', 'https://test.co,/test.jpg'
            )
        assert util.COMBINATION_ERROR == str(excinfo.value)

    @mock.patch('ricohcloudsdk.vrs.util.Image.open')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    def test_compare_faces_uuid_uuid(self, opn, isfile, pil_open):
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.side_effect = [False, False]
        with pytest.raises(ValueError) as excinfo:
            self.vrs.compare_faces(
                'ef0dce93-c2ac-4da5-bb2c-82ca7c770ad8', '06ef969b-4d2f-49bf-8f79-afc3bc072def'
            )
        assert util.COMBINATION_ERROR == str(excinfo.value)
