# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

from unittest import TestCase
import json
import pytest
import mock
from mock import Mock, MagicMock
from requests.exceptions import RequestException
from ricohcloudsdk.ips import util
from ricohcloudsdk.ips.client import ImageProcessing
from ricohcloudsdk.exceptions import ClientError

ENDPOINT = 'https://vps.api.ricoh/v1'


def make_headers(c_type):
    headers = {
        'Authorization': 'Bearer atoken',
        'x-api-key': 'apikey',
        'Accept': 'image/jpeg',
    }
    if c_type:
        headers['Content-Type'] = c_type
    return headers


class TestInit(TestCase):

    def setUp(self):
        self.aclient = Mock()
        self.aclient.session = Mock(return_value={'access_token': 'atoken'})

    def test_ok(self):
        ImageProcessing(self.aclient)

    def test_param_err(self):
        with pytest.raises(TypeError):
            ImageProcessing()


class TestMethodOK(TestCase):

    def setUp(self):
        self.aclient = Mock()
        self.aclient.get_access_token = Mock(return_value='atoken')
        self.aclient.get_api_key = Mock(return_value='apikey')
        self.aclient.session = Mock(return_value={'access_token': 'atoken'})
        self.ips = ImageProcessing(self.aclient)
        self.__parameters = {
            'locations': [{'left': 0, 'top': 0, 'right': 1, 'bottom': 1}],
            'type': 'blur',
            'options': {'ksize': 31}
        }
        self.__expected = b'image'

    def test_param_err(self):
        with pytest.raises(TypeError):
            self.ips.filter()

    @mock.patch('requests.post')
    def test_filter_uri(self, req):
        req.return_value.content = self.__expected
        req.return_value.status_code = 200
        assert self.__expected == self.ips.filter('http://test.com/test.jpg', self.__parameters)
        headers = make_headers('application/json')
        payload = json.dumps({'image': 'http://test.com/test.jpg', 'parameters': self.__parameters})
        req.assert_called_once_with(ENDPOINT + '/filter', headers=headers, data=payload)

    @mock.patch('imghdr.what')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.ips.client.open')
    @mock.patch('requests.post')
    def test_filter_jpeg(self, req, opn, isfile, imghdr):
        req.return_value.content = self.__expected
        req.return_value.status_code = 200
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        imghdr.return_value = 'jpeg'
        assert self.__expected == self.ips.filter('test.jpg', self.__parameters)
        isfile.assert_called_once_with('test.jpg')
        imghdr.assert_called_once_with('test.jpg')
        opn.assert_called_once_with('test.jpg', 'rb')
        headers = make_headers(None)
        files = {'image': ('test.jpg', opn(), 'image/jpeg')}
        data = {'parameters': json.dumps(self.__parameters)}
        req.assert_called_once_with(ENDPOINT + '/filter', headers=headers, files=files, data=data)

    @mock.patch('imghdr.what')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.ips.client.open')
    @mock.patch('requests.post')
    def test_filter_png(self, req, opn, isfile, imghdr):
        req.return_value.content = self.__expected
        req.return_value.status_code = 200
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        imghdr.return_value = 'png'
        assert self.__expected == self.ips.filter('test.png', self.__parameters)
        isfile.assert_called_once_with('test.png')
        imghdr.assert_called_once_with('test.png')
        opn.assert_called_once_with('test.png', 'rb')
        headers = make_headers(None)
        files = {'image': ('test.png', opn(), 'image/png')}
        data = {'parameters': json.dumps(self.__parameters)}
        req.assert_called_once_with(ENDPOINT + '/filter', headers=headers, files=files, data=data)


class TestMethodError(TestCase):

    def setUp(self):
        self.aclient = Mock()
        self.aclient.get_access_token = Mock(return_value='atoken')
        self.aclient.get_api_key = Mock(return_value='apikey')
        self.aclient.session = Mock(return_value={'access_token': 'atoken'})
        self.ips = ImageProcessing(self.aclient)
        self.__parameters = {
            'locations': [{'left': 0, 'top': 0, 'right': 1, 'bottom': 1}],
            'type': 'blur',
            'options': {'ksize': 31}
        }

    def test_filter_file_not_found(self):
        with pytest.raises(ValueError) as excinfo:
            self.ips.filter('image.jpg', self.__parameters)
        assert util.RESOURCE_ERROR == str(excinfo.value)

    @mock.patch('json.loads')
    @mock.patch('requests.post')
    def test_filter_resource_not_found(self, req, ret):
        req.return_value.text = 'test'
        req.return_value.status_code = 400
        ret.return_value = {'error': {'code': 'invalid_uri',
                                      'message': 'The requested URI does not represent any resource on the server.'}}
        try:
            self.ips.filter('http://test.com/test.jpg', self.__parameters)
        except ClientError as excinfo:
            assert ret.return_value == excinfo.response
            assert req.return_value.status_code == excinfo.status_code

    @mock.patch('imghdr.what')
    @mock.patch('os.path.isfile')
    @mock.patch('ricohcloudsdk.ips.client.open')
    @mock.patch('requests.post')
    def test_filter_gif(self, req, opn, isfile, imghdr):
        req.side_effect = RequestException
        opn.side_effect = mock.mock_open()
        opn.read_data = b'readdata'
        isfile.return_value = True
        imghdr.return_value = 'gif'
        with pytest.raises(ValueError) as excinfo:
            self.ips.filter('image.gif', self.__parameters)
        assert util.UNSUPPORTED_ERROR == str(excinfo.value)
