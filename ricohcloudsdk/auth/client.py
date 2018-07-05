# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

"""
RICOH Cloud API AUTH
"""

import time
import json
import requests
from requests.auth import HTTPBasicAuth


class AuthClient(object):
    """auth client"""
    __ENDPOINT = 'https://auth.api.ricoh'
    __MARGIN_SEC = 10

    SCOPES = {
        'vrs': ('ips.api.ricoh/v1/detect_faces',
                'ips.api.ricoh/v1/compare_faces',
                'ips.api.ricoh/v1/detect_humans'),
        'ips': ['vps.api.ricoh/v1/filter']
    }

    @staticmethod
    def __raise_value_error():
        raise ValueError('Could not get an access token to allow your access. '
                         'Make sure that your Client ID and Client Secret are correct.')

    def __init__(self, client_id, client_secret):
        self.__scopes = ''
        self.__grant_type = 'client_credentials'
        self.__bauth = HTTPBasicAuth(client_id, client_secret)
        self.__access_token = ''
        self.__api_key = ''
        self.__expire = 0

    def __auth(self):
        params = {
            'grant_type': self.__grant_type,
            'scope': self.__scopes
        }
        try:
            req = requests.post(AuthClient.__ENDPOINT +
                                '/v1/token',
                                auth=self.__bauth,
                                data=params)
            req.raise_for_status()
        except requests.exceptions.RequestException:
            raise
        try:
            ret = json.loads(req.text)
        except ValueError:
            AuthClient.__raise_value_error()
        return ret

    def __store_token_info(self, retval):
        try:
            self.__access_token = retval['access_token']
            self.__api_key = retval['api_key']
            self.__expire = retval['expires_in'] + \
                int(time.time()) - AuthClient.__MARGIN_SEC
        except KeyError:
            AuthClient.__raise_value_error()

    def session(self, scope):
        """Start session."""
        self.__scopes = ' '.join(scope)

        ret = self.__auth()
        self.__store_token_info(ret)
        return ret

    def get_access_token(self):
        """Get AccessToken."""
        if int(time.time()) < self.__expire:
            return self.__access_token

        ret = self.__auth()
        self.__store_token_info(ret)
        return self.__access_token

    def get_api_key(self):
        """Get APIKey."""
        if int(time.time()) < self.__expire:
            return self.__api_key

        ret = self.__auth()
        self.__store_token_info(ret)
        return self.__api_key
