# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

""" gaussian filter sample """
import os
import json
import argparse
from ricohcloudsdk.auth.client import AuthClient
from ricohcloudsdk.vrs.client import VisualRecognition
from ricohcloudsdk.ips.client import ImageProcessing


class HumanDetectionAndBlurFilterSample(object):
    """ human detection and blur filter sample """

    def __init__(self):
        """ read config file and initialize auth client """
        with open('./config.json', 'r') as settings:
            config = json.load(settings)
            client_id = config['CLIENT_ID']
            client_secret = config['CLIENT_SECRET']

        vrs_auth_client = AuthClient(client_id, client_secret)
        self.vrs_client = VisualRecognition(vrs_auth_client)

        ips_auth_client = AuthClient(client_id, client_secret)
        self.ips_client = ImageProcessing(ips_auth_client)

    def __detect_humans(self, img_path):
        res = self.vrs_client.detect_humans(img_path)
        return [human['location'] for human in res['humans']]

    def __blur_filter(self, img_path, options, locations):
        parameters = {'locations': locations, 'type': 'blur', 'options': options}
        res = self.ips_client.filter(img_path, parameters)
        return res

    def main(self):
        """ main """
        parser = argparse.ArgumentParser(description='Blur filter sample')
        parser.add_argument('-f', '--file', type=str, dest='file_path', help='specify image file (JPEG or PNG) to process')
        parser.add_argument('--ksize_width', type=int, dest='ksize_width', default=31, help='specify kernel size width')
        parser.add_argument('--ksize_height', type=int, dest='ksize_height', default=31, help='specify kernel size height')

        args = parser.parse_args()
        if args.file_path is None:
            parser.print_help()
            return

        locations = self.__detect_humans(args.file_path)

        options = {
            'locations': {
                'shape': 'min_enclosing_circle',
                'edge': 'blur'
            },
            'ksize_width': args.ksize_width,
            'ksize_height': args.ksize_height,
        }
        res = self.__blur_filter(args.file_path, options, locations)

        if not os.path.exists('./results'):
            os.mkdir('./results')
        with open('./results/human_detection_and_blur_filter.jpg', 'wb') as f:
            f.write(res)


if __name__ == '__main__':
    HumanDetectionAndBlurFilterSample().main()
