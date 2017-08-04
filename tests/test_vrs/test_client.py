# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

from unittest import TestCase
import json
import pytest
import mock
from mock import Mock, MagicMock
from requests.exceptions import RequestException
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
        self.__hd_expected = {
            'humans': [
                {
                    'score': 1,
                    'location': {
                        'top': 100,
                        'right': 200,
                        'bottom': 200,
                        'left': 100
                    }
                }
            ]
        }
        self.__fd_expected = {
            'faces': [
                {
                    'direction': 'left',
                    'location': {
                        'top': 100,
                        'right': 200,
                        'bottom': 200,
                        'left': 100
                    }
                }
            ]
        }
        self.__fr_expected = {
            "score": 0.787753701210022,
            "source": {
                "location": {
                    "left": 1085,
                    "top": 244,
                    "right": 1307,
                    "bottom": 466
                }
            },
            "target": {
                "location": {
                    "left": 659,
                    "top": 207,
                    "right": 812,
                    "bottom": 360
                }
            }
        }

    def test_param_err(self):
        with pytest.raises(TypeError):
            self.vrs.detect_faces()

    @mock.patch('requests.post')
    def test_detect_faces_uri(self, req):
        req.return_value.text = json.dumps(self.__fd_expected)
        req.return_value.status_code = 200
        assert self.__fd_expected == self.vrs.detect_faces(
            'http://test.com/test.jpg')
        headers = make_headers('application/json')
        payload = json.dumps({'image': 'http://test.com/test.jpg'})
        req.assert_called_once_with(
            ENDPOINT + '/detect_faces', headers=headers, data=payload)

    @mock.patch('imghdr.what')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    @mock.patch('requests.post')
    def test_detect_faces_jpeg(self, req, opn, isfile, imghdr):
        req.return_value.text = json.dumps(self.__fd_expected)
        req.return_value.status_code = 200
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        imghdr.return_value = 'jpeg'
        assert self.__fd_expected == self.vrs.detect_faces('test.jpg')
        isfile.assert_called_once_with('test.jpg')
        imghdr.assert_called_once_with('test.jpg')
        opn.assert_called_once_with('test.jpg', 'rb')
        headers = make_headers('image/jpeg')
        req.assert_called_once_with(
            ENDPOINT + '/detect_faces', headers=headers, data=opn())

    @mock.patch('imghdr.what')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    @mock.patch('requests.post')
    def test_detect_faces_png(self, req, opn, isfile, imghdr):
        req.return_value.text = json.dumps(self.__fd_expected)
        req.return_value.status_code = 200
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        imghdr.return_value = 'png'
        assert self.__fd_expected == self.vrs.detect_faces('test.png')
        isfile.assert_called_once_with('test.png')
        imghdr.assert_called_once_with('test.png')
        opn.assert_called_once_with('test.png', 'rb')
        headers = make_headers('image/png')
        req.assert_called_once_with(
            ENDPOINT + '/detect_faces', headers=headers, data=opn())

    @mock.patch('requests.post')
    def test_detect_humans_uri(self, req):
        req.return_value.text = json.dumps(self.__hd_expected)
        req.return_value.status_code = 200
        assert self.__hd_expected == self.vrs.detect_humans(
            'http://test.com/test.jpg')
        headers = make_headers('application/json')
        payload = json.dumps({'image': 'http://test.com/test.jpg'})
        req.assert_called_once_with(
            ENDPOINT + '/detect_humans', headers=headers, data=payload)

    @mock.patch('imghdr.what')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    @mock.patch('requests.post')
    def test_detect_humans_jpeg(self, req, opn, isfile, imghdr):
        req.return_value.text = json.dumps(self.__hd_expected)
        req.return_value.status_code = 200
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        imghdr.return_value = 'jpeg'
        assert self.__hd_expected == self.vrs.detect_humans('test.jpg')
        isfile.assert_called_once_with('test.jpg')
        imghdr.assert_called_once_with('test.jpg')
        opn.assert_called_once_with('test.jpg', 'rb')
        headers = make_headers('image/jpeg')
        req.assert_called_once_with(
            ENDPOINT + '/detect_humans', headers=headers, data=opn())

    @mock.patch('imghdr.what')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    @mock.patch('requests.post')
    def test_detect_humans_png(self, req, opn, isfile, imghdr):
        req.return_value.text = json.dumps(self.__hd_expected)
        req.return_value.status_code = 200
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        imghdr.return_value = 'png'
        assert self.__hd_expected == self.vrs.detect_humans('test.png')
        isfile.assert_called_once_with('test.png')
        imghdr.assert_called_once_with('test.png')
        opn.assert_called_once_with('test.png', 'rb')
        headers = make_headers('image/png')
        req.assert_called_once_with(
            ENDPOINT + '/detect_humans', headers=headers, data=opn())

    @mock.patch('requests.post')
    def test_compare_faces_uri(self, req):
        req.return_value.text = json.dumps(self.__fr_expected)
        req.return_value.status_code = 200
        assert self.__fr_expected == self.vrs.compare_faces(
            'http://test.com/test_1.jpg', 'http://test.com/test_2.jpg')
        headers = make_headers('application/json')
        payload = json.dumps(
            {
                'source': 'http://test.com/test_1.jpg',
                'target': 'http://test.com/test_2.jpg'
            }
        )
        req.assert_called_once_with(
            ENDPOINT + '/compare_faces', headers=headers, data=payload)

    @mock.patch('imghdr.what')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    @mock.patch('requests.post')
    def test_compare_faces_jpeg_jpeg(self, req, opn, isfile, imghdr):
        req.return_value.text = json.dumps(self.__fr_expected)
        req.return_value.status_code = 200
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        imghdr.return_value = 'jpeg'
        assert self.__fr_expected == self.vrs.compare_faces(
            'test_1.jpg', 'test_2.jpg'
        )
        headers = {
            'Authorization': 'Bearer atoken',
            'x-api-key': 'apikey'
        }
        payload = {
            'source': opn(),
            'target': opn()
        }
        req.assert_called_once_with(
            ENDPOINT + '/compare_faces', headers=headers, files=payload)

    @mock.patch('imghdr.what')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    @mock.patch('requests.post')
    def test_compare_faces_png_png(self, req, opn, isfile, imghdr):
        req.return_value.text = json.dumps(self.__fr_expected)
        req.return_value.status_code = 200
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        imghdr.return_value = 'png'
        assert self.__fr_expected == self.vrs.compare_faces(
            'test_1.png', 'test_2.png'
        )
        headers = {
            'Authorization': 'Bearer atoken',
            'x-api-key': 'apikey'
        }
        payload = {
            'source': opn(),
            'target': opn()
        }
        req.assert_called_once_with(
            ENDPOINT + '/compare_faces', headers=headers, files=payload)

    @mock.patch('imghdr.what')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    @mock.patch('requests.post')
    def test_compare_faces_jpeg_png(self, req, opn, isfile, imghdr):
        req.return_value.text = json.dumps(self.__fr_expected)
        req.return_value.status_code = 200
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        imghdr.side_effect = ['jpeg', 'png']
        assert self.__fr_expected == self.vrs.compare_faces(
            'test_1.jpeg', 'test_2.png'
        )
        headers = {
            'Authorization': 'Bearer atoken',
            'x-api-key': 'apikey'
        }
        payload = {
            'source': opn(),
            'target': opn()
        }
        req.assert_called_once_with(
            ENDPOINT + '/compare_faces', headers=headers, files=payload)


class TestMethodError(TestCase):

    def setUp(self):
        self.aclient = Mock()
        self.aclient.get_access_token = Mock(return_value='atoken')
        self.aclient.get_api_key = Mock(return_value='apikey')
        self.aclient.session = Mock(return_value={'access_token': 'atoken'})
        self.vrs = VisualRecognition(self.aclient)

    def test_detect_humans_file_not_found(self):
        with pytest.raises(ValueError):
            self.vrs.detect_humans('image.jpg')

    def test_detect_faces_file_not_found(self):
        with pytest.raises(ValueError):
            self.vrs.detect_faces('image.jpg')

    def test_compare_faces_file_not_found(self):
        with pytest.raises(ValueError):
            self.vrs.compare_faces('image_1.jpg', 'image_2.jpg')

    @mock.patch('json.loads')
    @mock.patch('requests.post')
    def test_detect_humans_resource_not_found(self, req, ret):
        req.return_value.text = 'test'
        req.return_value.status_code = 404
        ret.return_value = {'error': {'code': 'resource_not_found',
                                      'message': 'The specified resource does not exist.'}}
        with pytest.raises(ClientError):
            self.vrs.detect_humans('http://test.com/test.jpg')

    @mock.patch('json.loads')
    @mock.patch('requests.post')
    def test_detect_faces_resource_not_found(self, req, ret):
        req.return_value.text = 'test'
        req.return_value.status_code = 404
        ret.return_value = {'error': {'code': 'resource_not_found',
                                      'message': 'The specified resource does not exist.'}}
        with pytest.raises(ClientError):
            self.vrs.detect_faces('http://test.com/test.jpg')

    @mock.patch('json.loads')
    @mock.patch('requests.post')
    def test_compare_faces_resource_not_found(self, req, ret):
        req.return_value.text = 'test'
        req.return_value.status_code = 404
        ret.return_value = {'error': {'code': 'resource_not_found',
                                      'message': 'The specified resource does not exist.'}}
        with pytest.raises(ClientError):
            self.vrs.compare_faces(
                'http://test.com/test_1.jpg', 'http://test.com/test_2.jpg')

    @mock.patch('imghdr.what')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    @mock.patch('requests.post')
    def test_detect_humans_gif(self, req, opn, isfile, imghdr):
        req.side_effect = RequestException
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        imghdr.return_value = 'gif'
        with pytest.raises(ValueError):
            self.vrs.detect_humans('image.gif')

    @mock.patch('imghdr.what')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    @mock.patch('requests.post')
    def test_detect_faces_gif(self, req, opn, isfile, imghdr):
        req.side_effect = RequestException
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        imghdr.return_value = 'gif'
        with pytest.raises(ValueError):
            self.vrs.detect_faces('image.gif')

    @mock.patch('imghdr.what')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    @mock.patch('requests.post')
    def test_compare_faces_gif(self, req, opn, isfile, imghdr):
        req.side_effect = RequestException
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        imghdr.return_value = 'gif'
        with pytest.raises(ValueError):
            self.vrs.compare_faces('image_1.gif', 'image_2.gif')

    @mock.patch('imghdr.what')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.vrs.client.open')
    def test_compare_faces_jpeg_uri(self, opn, isfile, imghdr):
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.side_effect = [True, False]
        imghdr.return_value = 'jpeg'
        with pytest.raises(ValueError):
            self.vrs.compare_faces(
                'test_1.jpeg', 'https://test.co,/test.jpg'
            )
