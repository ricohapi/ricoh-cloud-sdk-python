# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

import json
from unittest import TestCase
import pytest
from requests.exceptions import RequestException
from ricohcloudsdk.auth.client import AuthClient
import mock

ENDPOINT = 'https://auth.api.ricoh/v1/token'
SCOPE = 'ips.api.ricoh/v1/detect_faces ips.api.ricoh/v1/compare_faces ips.api.ricoh/v1/detect_humans'


class TestInit(TestCase):

    def test_ok(self):
        AuthClient('client_id_test', 'client_secret_test')

    def test_param_err1(self):
        with pytest.raises(TypeError):
            AuthClient()

    def test_param_err2(self):
        with pytest.raises(TypeError):
            AuthClient('a')


class TestSession(TestCase):

    def setUp(self):
        self.target = AuthClient('client_id_test', 'client_secret_test')
        self.__expected = {
            'access_token': 'atoken',
            'api_key': 'api_key',
            'expires_in': 3600,
            'scope': SCOPE,
            'token_type': 'Bearer'
        }

    def __create_payload(self):
        payload = {
            'grant_type': 'client_credentials',
            'scope': SCOPE
        }
        return payload

    @mock.patch('requests.post')
    def test_ok(self, req):
        req.return_value.text = json.dumps(self.__expected)
        ret = self.target.session(AuthClient.SCOPES['vrs'])
        assert ret == self.__expected
        payload = self.__create_payload()
        req.assert_called_once_with(
            ENDPOINT, auth=self.target._AuthClient__bauth, data=payload)

    @mock.patch('requests.post')
    def test_json_exception(self, req):
        req.return_value.text = 'not json'
        with pytest.raises(ValueError):
            self.target.session(AuthClient.SCOPES['vrs'])
        payload = self.__create_payload()
        req.assert_called_once_with(
            ENDPOINT, auth=self.target._AuthClient__bauth, data=payload)

    @mock.patch('requests.post')
    def test_missing_expire_in(self, req):
        req.return_value.text = json.dumps(
            {
                'access_token': 'atoken',
                'api_key': 'api_key'
            }
        )
        with pytest.raises(ValueError):
            self.target.session(AuthClient.SCOPES['vrs'])
        payload = self.__create_payload()
        req.assert_called_once_with(
            ENDPOINT, auth=self.target._AuthClient__bauth, data=payload)

    @mock.patch('requests.post')
    def test_missing_keys(self, req):
        req.return_value.text = json.dumps(
            {
                'test': 'atoken'
            }
        )
        with pytest.raises(ValueError):
            self.target.session(AuthClient.SCOPES['vrs'])
        payload = self.__create_payload()
        req.assert_called_once_with(
            ENDPOINT, auth=self.target._AuthClient__bauth, data=payload)

    @mock.patch('requests.post')
    def test_requests_exception(self, req):
        req.side_effect = RequestException
        with pytest.raises(RequestException):
            self.target.session(AuthClient.SCOPES['vrs'])
        payload = self.__create_payload()
        req.assert_called_once_with(
            ENDPOINT, auth=self.target._AuthClient__bauth, data=payload)


class TestGetAccessToken(TestCase):

    def setUp(self):
        self.target = AuthClient('cid', 'cpass')
        self.__expected = {
            'access_token': 'atoken',
            'api_key': 'api_key',
            'expires_in': 3600,
            'scope': SCOPE,
            'token_type': 'Bearer'
        }

    @mock.patch('requests.post')
    def test_ok(self, req):
        req.return_value.text = json.dumps(self.__expected)
        self.target.session(AuthClient.SCOPES['vrs'])
        req.return_value.text = None
        ret = self.target.get_access_token()
        assert ret == 'atoken'

    @mock.patch('requests.post')
    def test_r_ok(self, req):
        req.return_value.text = json.dumps(self.__expected)
        ret = self.target.get_access_token()
        assert ret == 'atoken'

    @mock.patch('requests.post')
    def test_json_exception(self, req):
        req.return_value.text = 'not json'
        with pytest.raises(ValueError):
            ret = self.target.get_access_token()

    @mock.patch('requests.post')
    def test_exception(self, req):
        req.side_effect = RequestException
        with pytest.raises(RequestException):
            ret = self.target.get_access_token()


class TestGetAPIKey(TestCase):

    def setUp(self):
        self.target = AuthClient('cid', 'cpass')
        self.__expected = {
            'access_token': 'atoken',
            'api_key': 'api_key',
            'expires_in': 3600,
            'scope': SCOPE,
            'token_type': 'Bearer'
        }

    @mock.patch('requests.post')
    def test_ok(self, req):
        req.return_value.text = json.dumps(self.__expected)
        self.target.session(AuthClient.SCOPES['vrs'])
        req.return_value.text = None
        ret = self.target.get_api_key()
        assert ret == 'api_key'

    @mock.patch('requests.post')
    def test_r_ok(self, req):
        req.return_value.text = json.dumps(self.__expected)
        ret = self.target.get_api_key()
        assert ret == 'api_key'

    @mock.patch('requests.post')
    def test_json_exception(self, req):
        req.return_value.text = 'not json'
        with pytest.raises(ValueError):
            self.target.get_access_token()

    @mock.patch('requests.post')
    def test_exception(self, req):
        req.side_effect = RequestException
        with pytest.raises(RequestException):
            self.target.get_access_token()
