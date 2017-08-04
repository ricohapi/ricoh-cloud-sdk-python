# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

"""
Exceptions for RICOH Cloud SDK
"""


class BaseError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, status_code, response):
        _UNDEFINED = 'undefined'
        _MESSAGE = 'http_status: {status_code}, code: {code}, message: {message}'
        if not isinstance(response, dict):
            code = _UNDEFINED
            message = response
        elif 'message' in response:
            code = _UNDEFINED
            message = response.get('message', _UNDEFINED)
        elif 'error' in response:
            code = response['error'].get('code', _UNDEFINED),
            message = response['error'].get('message', _UNDEFINED)
        else:
            code = _UNDEFINED
            message = _UNDEFINED
        error_message = _MESSAGE.format(
            status_code=status_code,
            code=code,
            message=message
        )
        super(BaseError, self).__init__(error_message)
        self.status_code = status_code
        self.response = response


class ClientError(BaseError):
    """Exception raised for 4xx errors in the HTTP response."""
    pass


class ServerError(BaseError):
    """Exception raised for 5xx errors in the HTTP response."""
    pass
