# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

from unittest import TestCase
from ricohcloudsdk.exceptions import ClientError, ServerError


class TestSDKError(TestCase):

    def __make_sdk_error_message(self, status_code, code='undefined', message='undefined'):
        ERROR_TEMPLATE = 'http_status: {status_code}, code: {code}, message: {message}'
        sdk_error_message = ERROR_TEMPLATE.format(
            status_code=status_code,
            code=code,
            message=message
        )
        return sdk_error_message

    def test_client_error_normal(self):
        api_error_message = {'error': {'code': 'resource_not_found',
                                       'message': 'The specified resource does not exist.'}}
        sdk_error_message = self.__make_sdk_error_message(
            status_code='404',
            code='resource_not_found',
            message='The specified resource does not exist.'
        )
        try:
            raise ClientError(404, api_error_message)
        except ClientError as excinfo:
            assert 404 == excinfo.status_code
            assert api_error_message == excinfo.response
            assert sdk_error_message == excinfo.args[0]

    def test_client_error_only_message(self):
        api_error_message = {'message': 'Unsupported Media Type'}
        sdk_error_message = self.__make_sdk_error_message(
            status_code='415',
            message='Unsupported Media Type'
        )
        try:
            raise ClientError(415, api_error_message)
        except ClientError as excinfo:
            assert 415 == excinfo.status_code
            assert api_error_message == excinfo.response
            assert sdk_error_message == excinfo.args[0]

    def test_client_error_only_str(self):
        api_error_message = 'HTTP content length exceeded 10485760 bytes.'
        sdk_error_message = self.__make_sdk_error_message(
            status_code='413',
            message=api_error_message
        )
        try:
            raise ClientError(413, api_error_message)
        except ClientError as excinfo:
            assert 413 == excinfo.status_code
            assert api_error_message == excinfo.response
            assert sdk_error_message == excinfo.args[0]

    def test_server_error_normal(self):
        api_error_message = {'error': {'code': 'time_out',
                                       'message': 'The operation could not be completed within the acceptable time.'}}
        sdk_error_message = self.__make_sdk_error_message(
            status_code='500',
            code='time_out',
            message='The operation could not be completed within the acceptable time.'
        )
        try:
            raise ServerError(500, api_error_message)
        except ServerError as excinfo:
            assert 500 == excinfo.status_code
            assert api_error_message == excinfo.response
            assert sdk_error_message == excinfo.args[0]

    def test_server_error_only_message(self):
        api_error_message = {'message': 'Internal server error'}
        sdk_error_message = self.__make_sdk_error_message(
            status_code='500',
            message='Internal server error'
        )
        try:
            raise ServerError(500, api_error_message)
        except ServerError as excinfo:
            assert 500 == excinfo.status_code
            assert api_error_message == excinfo.response
            assert sdk_error_message == excinfo.args[0]
