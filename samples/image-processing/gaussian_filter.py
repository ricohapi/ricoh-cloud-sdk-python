# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

""" gaussian filter sample """
import os
import json
import argparse
from ricohcloudsdk.auth.client import AuthClient
from ricohcloudsdk.ips.client import ImageProcessing


class GaussianFilterSample(object):
    """ gaussian filter sample """

    def __init__(self):
        """ read config file and initialize auth client """
        with open('./config.json', 'r') as settings:
            config = json.load(settings)
            client_id = config['CLIENT_ID']
            client_secret = config['CLIENT_SECRET']

        self.auth_client = AuthClient(client_id, client_secret)
        self.ips_client = ImageProcessing(self.auth_client)

    def main(self):
        """ main """
        parser = argparse.ArgumentParser(description='Gaussian filter sample')
        parser.add_argument('-f', '--file', type=str, dest='file_path', help='specify image file (JPEG or PNG) to process')
        parser.add_argument('-t', '--location_top', type=int, dest='loc_top', help='specify locations top')
        parser.add_argument('-r', '--location_right', type=int, dest='loc_right', help='specify locations right')
        parser.add_argument('-b', '--location_bottom', type=int, dest='loc_bottom', help='specify locations bottom')
        parser.add_argument('-l', '--location_left', type=int, dest='loc_left', help='specify locations left')
        parser.add_argument('--ksize_width', type=int, dest='ksize_width', default=31, help='specify gaussian kernel size width')
        parser.add_argument('--ksize_height', type=int, dest='ksize_height', default=31, help='specify gaussian kernel size height')
        parser.add_argument('--sigma_x', type=float, dest='sigma_x', default=0, help='specify Gaussian kernel standard deviation in X direction')
        parser.add_argument('--sigma_y', type=float, dest='sigma_y', default=0, help='specify Gaussian kernel standard deviation in Y direction')
        args = parser.parse_args()
        if args.file_path is None \
                or args.loc_left is None \
                or args.loc_top is None \
                or args.loc_right is None \
                or args.loc_bottom is None:
            parser.print_help()
            return

        parameters = {
            'locations': [{
                'left': args.loc_left,
                'top': args.loc_top,
                'right': args.loc_right,
                'bottom': args.loc_bottom
            }],
            'type': 'gaussian',
            'options': {
                'locations': {
                    'shape': 'min_enclosing_circle',
                    'edge': 'blur'
                },
                'ksize_width': args.ksize_width,
                'ksize_height': args.ksize_height,
                'sigma_x': args.sigma_x,
                'sigma_y': args.sigma_y
            }
        }

        res = self.ips_client.filter(args.file_path, parameters)
        if not os.path.exists('./results'):
            os.mkdir('./results')
        with open('./results/image_filter.jpg', 'wb') as f:
            f.write(res)


if __name__ == '__main__':
    GaussianFilterSample().main()
